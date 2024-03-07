class Agent:
    def __init__(self, name, llm_config, instructions=None):
        self.name = name
        self.llm_config = llm_config
        self.instructions = instructions


class CoderAgent(Agent):
    def __init__(self, name, llm_config, file_id=None, instructions=None):
        super().__init__(name, llm_config, instructions)
        self.llm_config.update(
            {
                "request_timeout": 600,
                "temperature": 0,
                "tools": [{"type": "code_interpreter"}],
            }
        )
        if file_id:
            self.llm_config["file_ids"] = [file_id]


class CriticAgent(Agent):
    def __init__(self, name, llm_config, system_message):
        super().__init__(name, llm_config)
        self.system_message = system_message


class UserProxyAgent(Agent):
    def __init__(self, name, llm_config, is_termination_msg, code_execution_config):
        super().__init__(name, llm_config)
        self.is_termination_msg = is_termination_msg
        self.code_execution_config = code_execution_config

    def initiate_chat(self, manager, message, clear_history):
        if clear_history:
            manager.groupchat.messages.clear()
        manager.groupchat.messages.append({"sender": self.name, "content": message})


class GroupChatManager:
    def __init__(self, groupchat, llm_config):
        self.groupchat = groupchat
        self.llm_config = llm_config
