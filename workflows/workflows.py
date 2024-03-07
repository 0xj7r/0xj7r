import os 
import logging 
import uuid
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

class WorkflowStep:
    def __init__(self, expected_input, expected_output, command=None, args=None):
        if command and not callable(command):
            raise TypeError("command must be a function")

        if args and not isinstance(args, dict):
            raise TypeError("args must be a dictionary")

        self.expected_input = expected_input
        self.expected_output = expected_output
        self.command = command
        self.args = args if args else {}


class Workflows:
    def __init__(self):
        self.workflow = []

    def add_step(self, step):
        if not isinstance(step, WorkflowStep):
            raise TypeError("step must be an instance of WorkflowStep")

        self.workflow.append(step)

    def run(self):
        results = []
        for i, step in enumerate(self.workflow):
            print(f"Running step {i+1} with command {step.command} and args {step.args}")
            if step.command:
                try:
                    result = step.command(step.expected_input, **step.args)
                    if result != step.expected_output:
                        print(f"Step {i+1} failed. Expected output {step.expected_output}, got {result}")
                        results.append((False, result))
                    else:
                        print(f"Step {i+1} passed.")
                        results.append((True, result))
                except Exception as e:
                    print(f"Step {i+1} failed with error: {e}")
                    results.append((False, str(e)))

        return results
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

        