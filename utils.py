import sympy as sp


def to_cnf(formula):
    """
    Converts a logical premise to a CNF expression using sympy
    :param formula: Logical premise as a String. e.g. "(a v b) -> c"
    :return: a CNF expression representing the logical premise. Format is a list of sets or a set
    """
    cleaned_formula = clean_formula(formula)
    sympy_expr = sp.sympify(cleaned_formula)
    cnf_expr = sp.to_cnf(sympy_expr, simplify=True)
    cnf_expr = cnf_to_set(cnf_expr)
    return cnf_expr


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
    formula = formula.replace('→', '>>').replace('->', '>>').replace('implies', '>>')  # Turn implication to '>>'
    formula = formula.replace('¬', '~').replace('-', '~').replace('!', '~')  # Turn negation to '~'
    formula = formula.replace('V', '|').replace('v', '|').replace('∨', '|').replace('or', '|')  # Turn disjunction to '|'
    formula = formula.replace('∧', '&').replace('and', '&')  # Turn conjunction to '&'
    return formula


def cnf_to_set(expr):
    """
    Turns a sympy CNF expression into a set or list of sets for better access to its contents.
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
            literals.update(cnf_to_set(arg))
        return literals
    elif expr.func == sp.And:  # If expr is a conjunction
        # If it's a conjunction, iterate through each term to get disjunctions
        disjunctions = []
        for arg in expr.args:
            disjunctions.append(cnf_to_set(arg))
        return disjunctions
    else:
        return {str(expr)}


def set_to_cnf(cnf):
    """
        Converts a set or list of sets representing a CNF back to a Sympy CNF expression.
        :param cnf: A set or list of sets representing a CNF
        :return: A Sympy CNF expression
        """
    # If it's a single set, create a disjunction
    if isinstance(cnf, set):
        disjunction = sp.Or(*[sp.symbols(lit[1:]) if lit.startswith("~") else sp.symbols(lit) for lit in cnf])
        return disjunction

    # If it's a list of sets, create conjunctions of disjunctions
    conjunctions = []
    for disjunction_set in cnf:
        disjunction = sp.Or(
            *[sp.symbols(lit[1:]) if lit.startswith("~") else sp.symbols(lit) for lit in disjunction_set])
        conjunctions.append(disjunction)

    # Combine the disjunctions into a single CNF expression
    cnf_expr = sp.And(*conjunctions)

    return cnf_expr


def negate_expression(cnf_expr):
    if not isinstance(cnf_expr, sp.Expr):
        cnf_expr = set_to_cnf(cnf_expr)
    expr = sp.simplify_logic(~cnf_expr)
    return cnf_to_set(expr)


if __name__ == "__main__":
    formula = "(a | c) -> b"
    cnf_expr = to_cnf(formula)

    print("CNF:", cnf_expr)
    print("type:", type(cnf_expr))
    print(set_to_cnf(cnf_expr))
    expr2 = negate_expression(cnf_expr)
    print(expr2)
