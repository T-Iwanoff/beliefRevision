import textwrap
from belief_base import BeliefBase, Belief


PROMPT_INPUT = ">>> "


def print_help():
    text = """
        Belief Revision Engine
        -----------------------
        Available actions:
        p: Print current beliefs
        r: Revise current beliefs
        c: Clear the belief base
        h: Print this help dialog again
        q: Quit program
        """
    print(textwrap.dedent(text))


def handle_user_input(base: BeliefBase):
    while True:
        print("Select an action:")
        action = input(PROMPT_INPUT)

        if action == "p":
            print("Current beliefs:")
            for belief in base.beliefs:
                print(belief)
            if len(base.beliefs) == 0:
                print("No beliefs")
            print()
        elif action == "r":
            print("Revising beliefs...")
            print("Enter a formula:")
            formula = input(PROMPT_INPUT)
            try:
                print("set priority of belief (higher = more certain)")
                priority = int(input(PROMPT_INPUT))
                b = Belief(priority, formula)
                base.revise(b)
                print("Revision complete")
                print("Current belief base:")
                for belief in base.beliefs:
                    print(belief)
            except ValueError:
                print("Invalid formula")
            print()
        elif action == "c":
            base.clear()
            print("Belief base cleared")
            print()
        elif action == "h":
            print_help()
        elif action == "q":
            print("Quitting")
            exit()
        else:
            print("Invalid action")
            print()


if __name__ == '__main__':
    bb = BeliefBase()
    # Sample for filling out the belief base quickly
    # bb.add(Belief(formula="a | b"))

    print_help()
    handle_user_input(bb)
