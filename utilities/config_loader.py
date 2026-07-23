import yaml
from typing import Any
from utilities.logger import get_logger

logger = get_logger(__name__)

def load_config(config_path: str) -> dict[str,Any]:
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            logger.info(f"Loading configuration: {config_path}")
            config_obj = yaml.safe_load(file)
            logger.info("Configuration loaded successfully.")
        return config_obj
    except FileNotFoundError:
        logger.error(f"Error: The file '{config_path}' was not found. Please check the path.")
        raise
    except PermissionError:
        logger.error(f"Error: Permission denied when accessing '{config_path}'.")
        raise
    except OSError as e:
        logger.error(f"OS error occurred: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in configuration file: {config_path} - {e}") 
        raise