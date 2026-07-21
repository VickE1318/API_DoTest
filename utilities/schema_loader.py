import json
from typing import Any
from utilities.logger import get_logger
from pathlib import Path

logger = get_logger()

def load_schema(schema_name: str) -> dict[str,Any]:
    try:
        expected_schema_path = Path("baselines") / "schemas" / f"{schema_name}.json"
        with expected_schema_path.open("r", encoding="utf-8") as file:
            logger.info(f"Loading schema: {expected_schema_path}")
            schema_data = json.load(file)
            logger.info("Schema loaded successfully.")
        return schema_data
    
    except FileNotFoundError:
        logger.error(f"Error: The file '{expected_schema_path}' was not found. Please check the path.")
        raise 
    except PermissionError:
        logger.error(f"Error: Permission denied when accessing '{expected_schema_path}'.")
        raise
    except OSError as e:
        logger.error(f"OS error occurred: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in schema file: {expected_schema_path}")
        raise