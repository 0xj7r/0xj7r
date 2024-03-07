import autogen
from config_manager import ConfigManager
from file_manager import FileManager
from agents import CoderAgent, CriticAgent, UserProxyAgent, GroupChatManager
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Orchestrator:
    def __init__(self, agent_config, file_id=None):
        self.config_manager = ConfigManager("./config.json")
        self.agent_config = agent_config
        self.user_proxy = None
        self.file_id = file_id
        self.agents = []
        self.setup_agents()
        self.setup_group_chat()

    def setup_agents(self):
        if "coder" in self.agent_config:
            self.agents.append(
                CoderAgent(
                    "coder",
                    self.config_manager.llm_config,
                    self.file_id,
                    self.agent_config["coder"].get("instructions"),
                )
            )

        if "critic" in self.agent_config:
            self.agents.append(
                CriticAgent(
                    "critic",
                    self.config_manager.llm_config,
                    self.agent_config["critic"].get("system_message"),
                )
            )

        if "user" in self.agent_config:
            self.user_proxy = UserProxyAgent(
                "user",
                self.config_manager.llm_config,
                lambda msg: "TERMINATE" in msg["content"],
                {"work_dir": "assistant", "use_docker": False},
            )
            self.agents.append(self.user_proxy)

    def setup_group_chat(self):
        self.groupchat_manager = GroupChatManager(
            autogen.GroupChat(agents=self.agents, messages=[], max_round=20),
            self.config_manager.llm_config,
        )

    def run(self, user_message):
        if self.user_proxy:
            self.user_proxy.initiate_chat(
                self.groupchat_manager, user_message, clear_history=True
            )
        else:
            raise AttributeError("User proxy agent not initialized")
