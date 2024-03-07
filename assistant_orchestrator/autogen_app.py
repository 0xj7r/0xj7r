import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.agentchat import AssistantAgent, UserProxyAgent
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Initialise llm configs 
config_list = autogen.config_list_from_json(env_or_file="./config.json")
llm_config = {"config_list": config_list, "cache_seed": 42}

# Establish agents to use in network
coder_agent = GPTAssistantAgent(
    name="coder",
    llm_config={
        **llm_config,
        "request_timeout": 600,
        "temperature": 0,
        "tools": [{"type": "code_interpreter"}],
    },
    instructions="""
            You are an expert at writing python code.
            Consider best practices.
            Return the code in full. Do not exclude anything for brevity.
            Reply TERMINATE when the task is solved and there is no problem.
            """,
)
critic_agent = AssistantAgent(
    name="critic",
    system_message="""
    Critic. You are a helpful assistant highly skilled in evaluating the quality of a code output by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER BEST PRACTICES for the code, given the outcome that it is desgined to achieve. Specifically, you can carefully evaluate the code across the following dimensions
        - Bugs (bugs): are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
        - Model relevance (relevance): is the primary model used in the code the most relevant for the task? 
        - Goal compliance (compliance): how well the code meets the specified objectives?
        - Efficiency (efficiency): Is the code world-class in efficiency? Could it be improved using OOP best-practices?
        YOU MUST PROVIDE A SCORE for each of the above dimensions.
        {bugs: 0, relevance: 0, compliance: 0, efficiency: 0}
        Do not suggest code. 
        Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
    """,
    llm_config=llm_config,
)
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    code_execution_config={
        "work_dir": "assitant",
        "use_docker": False,
    },
    human_input_mode="NEVER",
)


if __name__ == "__main__":

    # Configure network
    groupchat = autogen.GroupChat(
        agents=[user_proxy, coder_agent, critic_agent], messages=[], max_round=20
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Initialise agent chat
    user_proxy.initiate_chat(
        manager,
        message="""
            Write me the Pyth
            Take the feedback from the critic to improve the code.
            Print the code.
            """,
        clear_history=True,
    )
