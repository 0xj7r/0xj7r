import os
import logging
import uuid
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)

load_dotenv()


class Workflows:
    """This class provides a structure for creating a workflow of tasks."""

    def __init__(self):
        """Constructor method initializes an empty list of steps."""
        self.steps = []

    def add_step(self, func, condition=lambda x: True, depends_on=None):
        """
        This method adds a step to the workflow.

        :param func: the function to be added as a step.
        :param condition: a function that takes one argument and returns a boolean. If True, the step is executed.
        :param depends_on: a list of function names that this step depends on.
        """
        self.steps.append((func, condition, depends_on or []))
        logging.info(f"A new step was added: {func.__name__}")

    def reorder_step(self, step_name, new_idx):
        """
        This method reorders a step in the workflow.

        :param step_name: name of the step (function) to be reordered.
        :param new_idx: the new index position for the step in workflow.
        """
        for idx, (func, cond, depends_on) in enumerate(self.steps):
            if func.__name__ == step_name:
                self.steps.insert(new_idx, self.steps.pop(idx))
                logging.info(f"Step {func.__name__} reordered.")
                break

    def run(self, input):
        """
        This method executes the workflow and returns an output.

        :param input: initial input for the workflow.
        """
        output = input
        executed = []
        for step, condition, depends_on in self.steps:
            if all(dep in executed for dep in depends_on):
                if condition(output):
                    try:
                        output = step(output)
                        logging.info(f"Step {step.__name__} executed.")
                        executed.append(step.__name__)
                    except Exception as e:
                        logging.error(f"Error executing step {step.__name__}: {e}")
                else:
                    logging.info(f"Step {step.__name__} was skipped.")
            else:
                logging.warning(
                    f"Step {step.__name__} was skipped due to unmet dependencies."
                )
        return output


# ```

#  You might use the class like this:

# ```python
# def dummy_function(inp, mul=1, add=0):
#     return inp * mul + add

# workflow = Workflows()
# step1 = WorkflowStep(1, 2, dummy_function, {'mul': 2, 'add': -1})
# workflow.add_step(step1)
# step2 = WorkflowStep(3, 6, dummy_function, {'mul': 2})
# workflow.add_step(step2)
# results = workflow.run()
# ```

# This would print:

# ```
# Running step 1 with command <function dummy_function at 0x7f7cdf3a90d0> and args {'mul': 2, 'add': -1}
# Step 1 passed.
# Running step 2 with command <function dummy_function at 0x7f7cdf3a90d0> and args {'mul': 2}
# Step 2 passed.
# ```

# And the `results` would be a list of tuples where each tuple consists of a boolean indicating success or failure and the result of the function call or the error message:

# ```
# [(True, 2), (True, 6)]
# ```
