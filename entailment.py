import utils
import sympy as sp
from belief_base import BeliefBase, Belief

def check_entailment(base, conclusion):
    # Convert premises and negated conclusion to CNF  # TODO Remove prints later
    cnf_premises = [belief.cnf for belief in base.beliefs]
    negated_conclusion = utils.negate_expression(conclusion)
    # print("premises:", cnf_premises)
    # print("negative:", negated_conclusion)

    # Combine premises with the negated conclusion
    clauses = set()
    if isinstance(negated_conclusion, list):
        for clause in negated_conclusion:
            clauses.add(frozenset(clause))
    else:
        clauses.add(frozenset(negated_conclusion))

    for belief in cnf_premises:
        if isinstance(belief, list):
            for clause in belief:
                clauses.add(frozenset(clause))
        else:
            clauses.add(frozenset(belief))

    # print("clauses:", clauses)
    # print("-----")

    # Set to keep track of derived clauses
    derived_clauses = set()

    # Loop until no new clauses are derived
    while True:
        new_clauses = set()

        # Try resolving each pair of clauses
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    resolved_clause = resolve_clauses(clause1, clause2)
                    # print("resolved clause:", resolved_clause)
                    if resolved_clause:
                        # print("------ found resolved clause ------")
                        new_clauses.update(frozenset(resolved_clause))
                        # print("new_clauses:", new_clauses)

        # Check for contradictions (empty clause)
        # print("Contradiction check")
        # print("new_clauses:", new_clauses)
        if set() in new_clauses:
            # print("empty clause, true")
            return True  # Logical entailment exists

        # If no new clauses are derived, no entailment
        # print("new clause check")
        if not new_clauses - derived_clauses:
            # print("nothing new, false")
            return False  # No logical entailment

        # Update clauses and derived clauses
        clauses.update(new_clauses)
        derived_clauses.update(new_clauses)


def resolve_clauses(Ci, Cj):
    """
        Returns the set of all possible clauses obtained by resolving Ci and Cj
        :param Ci: Clause 1, a set of literals
        :param Cj: Clause 2, a set of literals
        :return: A set of new clauses obtained by resolving Ci and Cj
        """
    clauses = set()  # Store all new clauses obtained by resolving
    for literal in Ci:
        # Check for complementary literals in the other clause
        if f'~{literal}' in Cj:
            # Create a new clause without the resolved literals
            new_clause = (Ci - {literal}) | (Cj - {f'~{literal}'})
            clauses.add(frozenset(new_clause))  # Use frozenset for immutability

    return clauses



if __name__ == '__main__':
    belief_base = BeliefBase()
    b1 = "a and b"
    b2 = "b -> c"
    c1 = utils.to_cnf(b1)
    c2 = utils.to_cnf(b2)
    belief_base.add(Belief(c1, b1))
    belief_base.add(Belief(c2, b2))
    print(belief_base.beliefs)
    print(check_entailment(belief_base, utils.to_cnf("b -> !a")))
    #print(resolve_clauses(c1[1], c2))
