import yaml
from loguru import logger


def load_config(file_path: str = './configs/local/config.yaml.'):
    with open(file_path, "r") as f:
        config =  yaml.safe_load(f)
        logger.info(config)
        return config
    
with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)