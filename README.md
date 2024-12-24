# CDCL SAT Solver
A Python implementation of a modern CDCL (Conflict-Driven Clause Learning) SAT solver with VSIDS (Variable State Independent Decaying Sum) decision heuristic and phase saving.

# Features

✨ CDCL (Conflict-Driven Clause Learning)

📊 VSIDS scoring for intelligent variable selection

🔄 Phase saving for better search efficiency

⚡ Non-chronological backtracking

🔍 Unit propagation

📝 Detailed debugging output

# Installation
No external dependencies required. Simply clone the repository:

```consol
git clone https://github.com/thePoland001/cdcl-sat-solver.git
cd cdcl-sat-solver
```

# Basic Usage

```python
from sat_solver import CDCLSolver

# Create a new solver instance
solver = CDCLSolver()

# Add clauses (each clause is a list of integers)
# Positive numbers represent positive literals (x₁)
# Negative numbers represent negative literals (¬x₁)
solver.add_clause([1, 2])    # x₁ ∨ x₂
solver.add_clause([-1, 3])   # ¬x₁ ∨ x₃
solver.add_clause([-2, -3])  # ¬x₂ ∨ ¬x₃

# Solve the formula
is_sat, assignment = solver.solve()

if is_sat:
    print("Formula is satisfiable!")
    print("Solution:", assignment)
else:
    print("Formula is unsatisfiable!")
```

# Example Output
```consol
Starting tests...

==================================================
Testing: Simple SAT case
Initializing solver...
Adding clause: [1, 2]
DEBUG: Added clause: [1, 2]
Adding clause: [-1, 3]
DEBUG: Added clause: [-1, 3]
Adding clause: [-2, -3]
DEBUG: Added clause: [-2, -3]
Adding clause: [2, 3]
DEBUG: Added clause: [2, 3]
Starting solve...
DEBUG: Starting solve
DEBUG: Decision: set 2 to True at level 1 (activity: 3.00)
DEBUG: Unit propagation: set 3 to False at level 1
DEBUG: Unit propagation: set 1 to False at level 1
DEBUG: Solution found - SAT
Is satisfiable? True
Assignment: {2: True, 3: False, 1: False}
Solution verification: PASSED

==================================================
Testing: UNSAT case
Initializing solver...
Adding clause: [1, 2]
DEBUG: Added clause: [1, 2]
Adding clause: [1, -2]
DEBUG: Added clause: [1, -2]
Adding clause: [-1, 2]
DEBUG: Added clause: [-1, 2]
Adding clause: [-1, -2]
DEBUG: Added clause: [-1, -2]
Starting solve...
DEBUG: Starting solve
DEBUG: Decision: set 1 to True at level 1 (activity: 4.00)
DEBUG: Unit propagation: set 2 to True at level 1
Is satisfiable? False

==================================================
Testing: Complex SAT case
Initializing solver...
Adding clause: [1, 2, 3]
DEBUG: Added clause: [1, 2, 3]
Adding clause: [-1, 2, 4]
DEBUG: Added clause: [-1, 2, 4]
Adding clause: [-2, 3, 4]
DEBUG: Added clause: [-2, 3, 4]
Adding clause: [-3, -4]
DEBUG: Added clause: [-3, -4]
Adding clause: [1, -2]
DEBUG: Added clause: [1, -2]
Adding clause: [2, -3]
DEBUG: Added clause: [2, -3]
Adding clause: [3, -4]
DEBUG: Added clause: [3, -4]
Starting solve...
DEBUG: Starting solve
DEBUG: Decision: set 2 to True at level 1 (activity: 5.00)
DEBUG: Unit propagation: set 1 to True at level 1
DEBUG: Decision: set 3 to True at level 2 (activity: 5.00)
DEBUG: Unit propagation: set 4 to False at level 2
DEBUG: Solution found - SAT
Is satisfiable? True
Assignment: {2: True, 1: True, 3: True, 4: False}
Solution verification: PASSED
```

Check the examples.py file for more usage examples
