import yaml
from loguru import logger


def load_config(file_path: str = "/code/configs/local/config.yaml") -> dict:
    """This function loads the config file

    Args:
        file_path (str, optional): The local config file. 
            Defaults to '/code/configs/local/config.yaml'.

    Returns:
        dict: The config file as a dictionary
    """
    with open(file_path, "r", encoding="utf-8") as f:
        yaml_config = yaml.safe_load(f)
        logger.info(yaml_config)
        return yaml_config


config = load_config()
