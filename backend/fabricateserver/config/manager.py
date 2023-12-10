import yaml
from loguru import logger
from fabricateserver.config import Config


def load_config(file_path: str = "/code/configs/local/config.yaml") -> Config:
    """This function loads the config file and returns a Config object.

    Args:
        file_path (str, optional): The local config file. 
            Defaults to '/code/configs/local/config.yaml'.

    Returns:
        Config: The config file as a Config object.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully.")
        return Config(**yaml_config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

 
config = load_config()

def save_config(new_config: Config, file_path: str = "/code/configs/local/config.yaml"):
    """This function saves the Config object to a YAML file.

    Args:
        config (Config): The configuration object to save.
        file_path (str, optional): The path to save the config file. 
            Defaults to '/code/configs/local/config.yaml'.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(new_config.__dict__, f)
        logger.info("Configuration saved successfully.")
        config = new_config
    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        raise
