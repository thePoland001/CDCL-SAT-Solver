class CDCLSolver:
    def __init__(self, debug=True):
        print("Initializing solver...")
        # Core solver state
        self.clauses = []          
        self.learned_clauses = []  
        self.assignments = {}      
        self.level = 0            
        self.decision_levels = {}  
        self.implications = {}    
        self.debug = debug
        
        # VSIDS scoring
        self.variable_activity = {} 
        self.var_inc = 1.0       
        self.var_decay = 0.95       
        
        # Phase saving
        self.saved_phases = {}      
        
    def log(self, message):
        if self.debug:
            print(f"DEBUG: {message}")
            
    def add_clause(self, clause):
        print(f"Adding clause: {clause}")
        self.clauses.append(clause)
        self.log(f"Added clause: {clause}")
        
        # Initializng VSIDS scores for variables in clause
        for lit in clause:
            var = abs(lit)
            if var not in self.variable_activity:
                self.variable_activity[var] = 0.0
            self._bump_variable_activity(var)
            
    def _bump_variable_activity(self, var):
        if var not in self.variable_activity:
            self.variable_activity[var] = 0.0
        self.variable_activity[var] += self.var_inc
        
        # Rescaling if activity gets too large
        if self.variable_activity[var] > 1e100:
            for v in self.variable_activity:
                self.variable_activity[v] *= 1e-100
            self.var_inc *= 1e-100
            
    def _decay_variables(self):
        self.var_inc *= (1.0 / self.var_decay)
            
    def _find_unit_clause(self):
        for clause in self.clauses + self.learned_clauses:
            unassigned = []
            is_satisfied = False
            
            for lit in clause:
                var = abs(lit)
                if var in self.assignments:
                    if (lit > 0) == self.assignments[var]:
                        is_satisfied = True
                        break
                else:
                    unassigned.append(lit)
            
            if not is_satisfied and len(unassigned) == 1:
                return unassigned[0], clause
                
        return None, None
            
    def _unit_propagation(self):
        while True:
            unit_lit, reason = self._find_unit_clause()
            if unit_lit is None:
                break
                
            var = abs(unit_lit)
            value = unit_lit > 0
            
            # Checking for conflict
            if var in self.assignments:
                if self.assignments[var] != value:
                    return False, reason
                continue
            
            # Making assignment
            self.assignments[var] = value
            self.decision_levels[var] = self.level
            self.implications[var] = reason
            self.saved_phases[var] = value  
            self.log(f"Unit propagation: set {var} to {value} at level {self.level}")
            
        return True, None
            
    def _analyze_conflict(self, conflict_clause):
        self.log(f"Analyzing conflict from clause: {conflict_clause}")
        
        # Tracking variables from current decision level
        current_level_vars = set()
        other_level_lits = []
        
        # Initializing from conflict clause
        for lit in conflict_clause:
            var = abs(lit)
            if self.decision_levels[var] == self.level:
                current_level_vars.add(var)
                self._bump_variable_activity(var)  
            else:
                other_level_lits.append(lit)
                
  
        while len(current_level_vars) > 1:
            # Pick latest assigned variable
            var = max(current_level_vars, key=lambda v: self.decision_levels[v])
            current_level_vars.remove(var)
            
            if var in self.implications:
                antecedent = self.implications[var]
                for lit in antecedent:
                    var_ant = abs(lit)
                    if var_ant != var:
                        if self.decision_levels[var_ant] == self.level:
                            current_level_vars.add(var_ant)
                            self._bump_variable_activity(var_ant)
                        else:
                            other_level_lits.append(lit)
        
      
        if current_level_vars:
            var = current_level_vars.pop()
            learned_lit = -var if self.assignments[var] else var
            learned_clause = other_level_lits + [learned_lit]
            
            self.log(f"Learned clause: {learned_clause}")
            return learned_clause
        
        return other_level_lits
            
    def _backtrack(self, level):
        self.log(f"Backtracking to level {level}")
        
        for var in list(self.assignments.keys()):
            if self.decision_levels[var] > level:
                # Save phase before unassigning
                self.saved_phases[var] = self.assignments[var]
                del self.assignments[var]
                del self.decision_levels[var]
                if var in self.implications:
                    del self.implications[var]
                    
        self.level = level
            
    def _find_unassigned_var(self):
        max_activity = -1
        chosen_var = None
        
        for var in self.variable_activity:
            if var not in self.assignments and self.variable_activity[var] > max_activity:
                max_activity = self.variable_activity[var]
                chosen_var = var
                
        return chosen_var
            
    def solve(self):
        """Main SAT solving function"""
        self.log("Starting solve")
        self.level = 0
        self.assignments = {}
        self.decision_levels = {}
        self.implications = {}
        
        while True:
            success, conflict_clause = self._unit_propagation()
            
            if not success:
                if self.level == 0:
                    self.log("Conflict at level 0 - UNSAT")
                    return False, {}
                    
                learned_clause = self._analyze_conflict(conflict_clause)
                self.learned_clauses.append(learned_clause)
                
                # Finding backtrack level
                if len(learned_clause) == 1:
                    backtrack_level = 0
                else:
                    levels = [self.decision_levels[abs(lit)] for lit in learned_clause]
                    levels.remove(max(levels))
                    backtrack_level = max(levels) if levels else 0
                    
                # Backtrack non-chronologically
                self._backtrack(backtrack_level)
                continue
            
            var = self._find_unassigned_var()
            
            if var is None:
                if self._verify_solution():
                    self.log("Solution found - SAT")
                    return True, self.assignments.copy()
                return False, {}
            
            # Make new decision using phase saving
            self.level += 1
            value = self.saved_phases.get(var, True)  
            self.assignments[var] = value
            self.decision_levels[var] = self.level
            self.log(f"Decision: set {var} to {value} at level {self.level} (activity: {self.variable_activity[var]:.2f})")
            
            self._decay_variables()
            
    def _verify_solution(self):
        for clause in self.clauses + self.learned_clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in self.assignments and (lit > 0) == self.assignments[var]:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True
