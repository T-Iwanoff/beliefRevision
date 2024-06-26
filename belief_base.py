import utils
import contraction
import expansion

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

    def revise(self, belief):
        """
        Performs belief revision using Levi's Identity
        :param belief: the belief to added
        """
        contraction.contract(self, ~belief)
        expansion.expansion(self, belief)


class Belief:
    def __init__(self, priority=0, formula=None):
        self.formula = formula
        self.cnf = utils.to_cnf(formula)
        self.priority = priority

    def __eq__(self, other):
        return self.cnf == other.cnf

    def __repr__(self):
        return f'Formula: {self.formula}, CNF: {self.cnf}, priority: {self.priority}'

    def __invert__(self):
        return Belief(priority=self.priority, formula=f"!({self.formula})")


if __name__ == "__main__":
    base = BeliefBase()
    print(base.beliefs)
    b1 = Belief(formula="a", priority=2)
    b2 = Belief(formula="!a", priority=1)
    base.add(b1)
    base.revise(b2)
    #base.add(b2)
    #print(base.beliefs)

   