import sympy as sp


def to_cnf(formula):
    """
    Converts a logical premise to a CNF formula using sympy
    :param formula: Logical premise as a String. e.g. (a v b) -> c
    :return: a CNF expression representing the logical premise. Format is Or or And
    """
    cleaned_formula = clean_formula(formula)
    sympy_expr = sp.sympify(cleaned_formula)
    cnf_expr = sp.to_cnf(sympy_expr, simplify=True)
    return parse_cnf(cnf_expr)


def is_cnf(formula):
    """
    Checks whether a logical premise is in CNF format
    :param formula: the logical premise
    :return: boolean
    """
    pass  # TODO in case we need it


def clean_formula(formula):
    """
    Ensures the logical premise is readable by sympy by enforcing its way of representing logical connectives
    :param formula: The logical premise as a String
    :return: The logical premise as a String
    """
    # formula = formula.replace('↔', '<=>').replace('<->', '<=>')  # Turn biconditional equivalence to '<=>' TODO This doesn't work
    formula = formula.replace('→', '>>').replace('->', '>>')  # Turn implication to '>>'
    formula = formula.replace('¬', '~').replace('-', '~').replace('!', '~')  # Turn negation to '~'
    formula = formula.replace('V', '|').replace('v', '|').replace('∨', '|')  # Turn disjunction to '|'
    formula = formula.replace('∧', '&')  # Turn conjunction to '&'
    return formula


def parse_cnf(expr):
    """
    Turns a sympy CNF formula into a set or list of sets for better access to its contents.
    If the formula includes disjunctions, it returns a list of sets. If not, it returns a set
    :param expr: The CNF formula as a sympy expression
    :return: A set or list of sets
    """
    if expr.is_Atom:  # If expr is a simple premise
        return {str(expr)}
    elif expr.func == sp.Not:  # If expr is a negation
        return {f'~{expr.args[0]}'}
    elif expr.func == sp.Or:  # If expr is a disjunction
        # For disjunctions, return a set of literals
        literals = set()
        for arg in expr.args:
            literals.update(parse_cnf(arg))
        return literals
    elif expr.func == sp.And:  # If expr is a conjunction
        # If it's a conjunction, iterate through each term to get disjunctions
        disjunctions = []
        for arg in expr.args:
            disjunctions.append(parse_cnf(arg))
        return disjunctions
    else:
        return {str(expr)}


if __name__ == "__main__":
    formula = "(a | c) -> b"
    cnf_expr = to_cnf(formula)

    print("CNF:", cnf_expr)
    print("type:", type(cnf_expr))
