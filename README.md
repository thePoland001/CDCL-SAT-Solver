# CDCL-SAT-Solver

A Python implementation of a CDCL (Conflict-Driven Clause Learning) SAT solver with VSIDS heuristics and phase saving. This solver efficiently determines if a boolean formula in conjunctive normal form (CNF) is satisfiable.

# Features

CDCL (Conflict-Driven Clause Learning)
VSIDS (Variable State Independent Decaying Sum) heuristics
Phase saving
Non-chronological backtracking
Unit propagation
Comprehensive documentation
Example usage and test cases

# Installation
No external dependencies required. Simply clone the repository:

```consol
git clone https://github.com/thePoland001/cdcl-sat-solver.git
cd cdcl-sat-solver
```
# Usage
The solver accepts boolean formulas in CNF (Conjunctive Normal Form). Each clause is represented as a list of integers, where positive numbers represent positive literals and negative numbers represent negative literals.

```consol
from sat_solver import solve_cnf

# Example: (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (¬x₂ ∨ ¬x₃)
clauses = [
    [1, 2],    # x₁ ∨ x₂
    [-1, 3],   # ¬x₁ ∨ x₃
    [-2, -3]   # ¬x₂ ∨ ¬x₃
]

is_sat, assignment = solve_cnf(clauses)

if is_sat:
    print("Formula is satisfiable!")
    print("Solution:", assignment)
else:
    print("Formula is unsatisfiable!")
```
# Using the Solver Class Directly
You can also use the CDCLSolver class directly for more control:
```python
from sat_solver import CDCLSolver

solver = CDCLSolver()

# Add clauses one by one
solver.add_clause([1, 2])     # x₁ ∨ x₂
solver.add_clause([-1, 3])    # ¬x₁ ∨ x₃
solver.add_clause([-2, -3])   # ¬x₂ ∨ ¬x₃

# Solve the formula
is_sat, assignment = solver.solve()
```

# Handling DIMACS Format
Here's a utility function to read DIMACS format files:

```python
def read_dimacs(filename):
    clauses = []
    with open(filename, 'r') as f:
        for line in f:
            # Skip comments and problem line
            if line.startswith('c') or line.startswith('p'):
                continue
            # Parse clause
            clause = [int(x) for x in line.strip().split()[:-1]]  # Remove trailing 0
            if clause:  # Skip empty lines
                clauses.append(clause)
    return clauses

# Usage
clauses = read_dimacs('example.cnf')
is_sat, assignment = solve_cnf(clauses)
```

