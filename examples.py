"""
Example usage of the CDCL SAT solver.
This file contains various test cases and examples showing different features.
"""

from sat_solver import CDCLSolver

def run_example(name, clauses):
    """Run a single example and print results."""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    solver = CDCLSolver()
    
    for clause in clauses:
        solver.add_clause(clause)
        
    print("Starting solve...")
    is_sat, assignment = solver.solve()
    print(f"Is satisfiable? {is_sat}")
    
    if is_sat:
        print(f"Assignment: {assignment}")
        
        # Verify solution
        valid = True
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if (lit > 0) == assignment[var]:
                    satisfied = True
                    break
            if not satisfied:
                print(f"ERROR: Clause {clause} not satisfied!")
                valid = False
        print(f"Solution verification: {'PASSED' if valid else 'FAILED'}")

def main():
    """Run all examples."""
    examples = [
        {
            "name": "Simple SAT case",
            "description": "Basic satisfiable formula: (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (¬x₂ ∨ ¬x₃)",
            "clauses": [
                [1, 2],    # x₁ ∨ x₂
                [-1, 3],   # ¬x₁ ∨ x₃
                [-2, -3]   # ¬x₂ ∨ ¬x₃
            ]
        },
        {
            "name": "Simple UNSAT case",
            "description": "Basic unsatisfiable formula: (x₁) ∧ (¬x₁)",
            "clauses": [
                [1],       # x₁
                [-1]       # ¬x₁
            ]
        },
        {
            "name": "Unit Propagation Example",
            "description": "Formula requiring unit propagation: (x₁) ∧ (¬x₁ ∨ x₂) ∧ (¬x₂ ∨ x₃)",
            "clauses": [
                [1],       # x₁
                [-1, 2],   # ¬x₁ ∨ x₂
                [-2, 3]    # ¬x₂ ∨ x₃
            ]
        },
        {
            "name": "Complex SAT case",
            "description": "More complex formula requiring learning",
            "clauses": [
                [1, 2, 3],    # x₁ ∨ x₂ ∨ x₃
                [-1, 2, 4],   # ¬x₁ ∨ x₂ ∨ x₄
                [-2, 3, 4],   # ¬x₂ ∨ x₃ ∨ x₄
                [-3, -4],     # ¬x₃ ∨ ¬x₄
                [1, -2],      # x₁ ∨ ¬x₂
                [2, -3],      # x₂ ∨ ¬x₃
                [3, -4]       # x₃ ∨ ¬x₄
            ]
        },
        {
            "name": "VSIDS Test",
            "description": "Formula to demonstrate VSIDS decision making",
            "clauses": [
                [1, 2],     # x₁ ∨ x₂
                [1, -2],    # x₁ ∨ ¬x₂
                [-1, 2],    # ¬x₁ ∨ x₂
                [-1, 3],    # ¬x₁ ∨ x₃
                [2, 3],     # x₂ ∨ x₃
                [-2, -3]    # ¬x₂ ∨ ¬x₃
            ]
        }
    ]
    
    print("CDCL SAT Solver Examples")
    print("=" * 50)
    
    for example in examples:
        print(f"\nRunning: {example['name']}")
        print(f"Description: {example['description']}")
        run_example(example['name'], example['clauses'])

if __name__ == "__main__":
    main()
