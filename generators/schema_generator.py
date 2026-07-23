import json
from pathlib import Path
from utilities.logger import get_logger

logger = get_logger(__name__)

class SchemaGenerator:
    def generate_schema(self, actual_data):
        actual_schema={}
        for key,actual_value in actual_data.items():
            if isinstance(actual_value,dict):
                nested_dict_schema=self.generate_schema(actual_value)
                actual_schema[key]=nested_dict_schema
            elif isinstance(actual_value,list):
                if actual_value:
                    first_item = actual_value[0]
                    if isinstance(first_item,dict):
                        nested_list_schema=self.generate_schema(first_item)
                        actual_schema[key]=[nested_list_schema]
                    else:
                        actual_schema[key]=[type(first_item).__name__]
                else:
                    actual_schema[key]=[]
            else:
                actual_schema[key]=type(actual_value).__name__
        return actual_schema
    
    def save_schema(self,schema_data,schema_name):
        schema_directory = Path("baselines") / "schemas"
        schema_directory.mkdir(parents=True, exist_ok=True)
        schema_file_path = schema_directory / f"{schema_name}.json"
        try:
            with schema_file_path.open("w", encoding="utf-8") as f:
                json.dump(schema_data, f, indent=4)
            logger.info(f"Schema file {schema_name} successfully saved to: {schema_file_path}")
        except OSError as e:
            logger.error(f"Failed to write schema to {schema_file_path}: {e}")
            raise
