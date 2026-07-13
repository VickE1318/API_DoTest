import yaml
from pathlib import Path
from typing import Any

def load_config(config_path: str) -> dict[str,Any]:
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config_obj = yaml.safe_load(file)
        return config_obj
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{config_path}' was not found. Please check the path.")
    except PermissionError:
        raise PermissionError(f"Error: Permission denied when accessing '{config_path}'.")
    except OSError as e:
        raise OSError(f"OS error occurred: {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in configuration file: {config_path}") from e