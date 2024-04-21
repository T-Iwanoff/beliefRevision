

def check_entailment(base, formula):
    pass


def resolve_clauses(C1, C2):
    # Find literals where one clause has a positive, and the other has the negation
    resolvable_literals = [literal for literal in C1 if -literal in C2]  # TODO -literals probably doesn't work
    if not resolvable_literals:
        return None

    # Joins the clauses and removes the contradictory literals found above
    resolved_clauses = (C1 | C2) - set(resolvable_literals) - set([-literal for literal in resolvable_literals])
    return resolved_clauses

