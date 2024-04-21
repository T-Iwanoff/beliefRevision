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
        Removes a belief from the belief base.
        :param belief: A Belief object
        """
        for b in self.beliefs:
            if b == belief:
                self.beliefs.remove(belief)






class Belief:
    def __init__(self, formula, cnf):
        self.formula = formula
        self.cnf = cnf

    def __eq__(self, other):
        return self.formula == other.formula

    def __repr__(self):
        return self.formula


if __name__ == "__main__":
    belief = BeliefBase()
    b = Belief(formula="a | b", cnf=utils.to_cnf("a | b"))
    belief.add()