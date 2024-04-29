from entailment import validate_base
from belief_base import BeliefBase, Belief


def contract(base, belief):
    """
    Contracts the belief base based on the priority of the beliefs.

    :param base: A belief base
    :param belief: The belief to be removed from the belief base.
    :return: contracted belief base
    """

    def criterion(belief):  
        return belief.priority

    base.discard(belief)

    current_base = base
    contradictory = not validate_base(current_base)

    while contradictory and current_base:
        min_priority = min(criterion(b) for b in current_base)
        candidates = [b for b in current_base if criterion(b) == min_priority]

        belief_to_contract = candidates[0]

        current_base.remove(belief_to_contract)

        contradictory = not validate_base(current_base)

    return current_base


if __name__ == '__main__':
    belief_base = BeliefBase()

    b1 = Belief(formula="a", priority=2)
    b2 = Belief(formula="b", priority=1)
    b3 = Belief(formula="a -> b", priority=3)
    belief_base.add(b1)
    belief_base.add(b2)
    belief_base.add(b3)
    contracted_base = contract(belief_base, b1)
    print(contracted_base.beliefs)

