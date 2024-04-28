import utils

from entailment import validate_base
from belief_base import BeliefBase, Belief

def expansion(base, belief):
    """
    Expands the belief base by adding the new belief, if it does not contradict with belief base

    :param base: A belief base
    :param belief: The belief to be added to the belief base.
    :return: expanded belief base
    """
    
    new_base = BeliefBase()
    for i in base.beliefs:
        new_base.add(i)
    new_base.add(belief)

    if validate_base(new_base):
        return new_base
    else:
        return base

if __name__ == '__main__':
    belief_base = BeliefBase()

    b1 = Belief(formula="a", cnf=utils.to_cnf("a"), priority=2)
    b2 = Belief(formula="b", cnf=utils.to_cnf("b"), priority=1)
    b3 = Belief(formula="c", cnf=utils.to_cnf("c"), priority=3)
    belief_base.add(b1)
    belief_base.add(b2)
    expanded_base = expansion(belief_base, b3)
    #b3 should be in expanded base
    print(expanded_base.beliefs)
