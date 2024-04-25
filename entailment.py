import utils
from belief_base import BeliefBase, Belief


def check_entailment(base, conclusion):
    """ TODO Remove prints later
    Checks whether a given base entails a conclusion.
    :param base: A belief base
    :param conclusion: A cnf expression (set or sympy expr)
    :return: True if the base entails a conclusion, false if it leads to a contradiction
    """
    # Convert premises and negative conclusion to sets
    cnf_premises = [belief.cnf for belief in base.beliefs]
    negated_conclusion = utils.negate_expression(conclusion)

    # Combine the premises with the negative conclusion
    clauses = set()

    for belief in cnf_premises:
        if isinstance(belief, list):
            for clause in belief:
                clauses.add(frozenset(clause))
        else:
            clauses.add(frozenset(belief))
    if isinstance(negated_conclusion, list):
        for clause in negated_conclusion:
            clauses.add(frozenset(clause))
    else:
        clauses.add(frozenset(negated_conclusion))

    print("premises:", cnf_premises)
    print("negative:", negated_conclusion)

    print("clauses:", clauses)
    print("-----")

    # Look for contradictions. If a contradiction is found (with the negated conclusion), the entailment holds
    return not _find_contradiction(clauses)


def validate_base(base):
    """
    Checks whether a base is contradictory. Returns true if the base is valid
    :param base: A belief base
    :return: Boolean indicating whether a base is valid or contradictory
    """
    # Turn the belief base into a set of frozensets
    cnf_premises = [belief.cnf for belief in base.beliefs]
    clauses = set()
    for belief in cnf_premises:
        if isinstance(belief, list):
            for clause in belief:
                clauses.add(frozenset(clause))
        else:
            clauses.add(frozenset(belief))

    # If there are no contradictions, return true
    return not _find_contradiction(clauses)


def _find_contradiction(clauses):
    """
    Returns whether a set of clauses contains a contradiction
    :param clauses: A set containing frozensets of literals. Each frozenset equates to a clause
    :return: Boolean indicating whether the clauses contain a contradiction
    """
    # Set to keep track of derived clauses
    derived_clauses = set()

    # Loop until no new clauses are derived
    while True:
        new_clauses = set()

        # Try resolving each pair of clauses
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    resolved_clause = _resolve_clauses(clause1, clause2)
                    if resolved_clause:
                        new_clauses.update(frozenset(resolved_clause))

        # Check for contradictions (empty clause)
        # print("Contradiction check")
        # print("new_clauses:", new_clauses)
        # print(type(new_clauses))
        if set() in new_clauses:
            # print("empty clause, true")
            return True

        # If no new clauses are derived, return false
        # print("new clause check")
        if not new_clauses - derived_clauses:
            # print("nothing new, false")
            return False  # No contradictions in the provided clauses

        # Update clauses and derived clauses
        clauses.update(new_clauses)
        derived_clauses.update(new_clauses)


def _resolve_clauses(ci, cj):
    """
        Returns the set of all possible clauses obtained by resolving Ci and Cj
        :param ci: Clause 1, a set of literals
        :param cj: Clause 2, a set of literals
        :return: A set of new clauses obtained by resolving Ci and Cj
        """
    clauses = set()  # Store all new clauses obtained by resolving
    for literal in ci:
        # Check for complementary literals in the other clause
        if f'~{literal}' in cj:
            # Create a new clause without the resolved literals
            new_clause = (ci - {literal}) | (cj - {f'~{literal}'})
            clauses.add(frozenset(new_clause))  # Use frozenset for immutability

    return clauses


if __name__ == '__main__':
    belief_base = BeliefBase()
    b1 = "c"
    b2 = "!a"
    c1 = utils.to_cnf(b1)
    c2 = utils.to_cnf(b2)
    belief_base.add(Belief(c1, b1))
    belief_base.add(Belief(c2, b2))
    print("base:", belief_base.beliefs)
    print(check_entailment(belief_base, utils.to_cnf("!b")))
    # print("Is base valid?", validate_base(belief_base))
