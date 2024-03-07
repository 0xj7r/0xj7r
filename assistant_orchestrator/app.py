from openai import OpenAI
from file_manager import FileManager
from orchestrator import Orchestrator
from starting_prompts import prompts
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

if __name__ == "__main__":

    # Set agent config
    agent_config = {
        "coder": {"use_file": True, "instructions": prompts["coder"]},
        "critic": {"system_message": prompts["critic"]},
        "user": {}
    }

    # Run app
    app = Orchestrator(agent_config)
    app.run(user_message="Write me the Python code to calculate 1+2")
