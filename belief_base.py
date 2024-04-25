import utils


class BeliefBase:

    def __init__(self):
        self.beliefs = []

    def add(self, belief):
        """
        Adds a belief to the belief base. Does not validate the belief base
        :param belief: A Belief object
        """
        self.discard(belief)
        self.beliefs.append(belief)

    def discard(self, belief):
        """
        Removes a belief from the belief base. If there are multiple identical beliefs,
        removes all of them.
        :param belief: A Belief object
        """
        for b in self.beliefs:
            if b == belief:
                self.beliefs.remove(belief)

    def clear(self):
        """
        Empties the belief base.
        """
        self.beliefs.clear()

    def expand(self, belief):
        pass

    def contract(self, belief):
        pass

    def revise(self, belief):
        pass


class Belief:
    def __init__(self, cnf, formula=None):
        self.formula = formula
        self.cnf = cnf

    def __eq__(self, other):
        return self.cnf == other.cnf

    def __repr__(self):
        return f'Formula: {self.formula}, CNF: {self.cnf}'


if __name__ == "__main__":
    base = BeliefBase()
    print(base.beliefs)
    b1 = Belief(formula="a | b", cnf=utils.to_cnf("a | b"))
    b2 = Belief(formula="b | a", cnf=utils.to_cnf("b | a"))
    base.add(b1)
    base.add(b2)
    print(base.beliefs)
