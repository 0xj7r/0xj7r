import autogen


class ConfigManager:
    def __init__(self, config_path):
        self.config_list = autogen.config_list_from_json(env_or_file=config_path)
        self.llm_config = {"config_list": self.config_list, "cache_seed": 42}
