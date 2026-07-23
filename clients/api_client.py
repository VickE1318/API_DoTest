import requests
from utilities.logger import get_logger
from validators.schema_validator import SchemaValidator
from utilities.schema_loader import load_schema,schema_exists
from generators.schema_generator import SchemaGenerator
from utilities.allure_helper import *

logger = get_logger(__name__)

class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.validator = SchemaValidator()
        self.generator = SchemaGenerator()

    def request(self, method, endpoint, expected_schema=None, schema_name=None, auto_generate=False, **kwargs):
        #Load schema
        if expected_schema and schema_name:
            logger.error("Provide either expected_schema or schema_name, not both.")
            raise ValueError("Provide either expected_schema or schema_name, not both.")
        elif schema_name:
            if schema_exists(schema_name):
                expected_schema=load_schema(schema_name)
                logger.info(f"Using baseline schema '{schema_name}'")
            else:
                logger.warning(f"Baseline schema '{schema_name}' not found")

       #Endpoint formation
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = self.base_url + endpoint
        attach_request(method,url)
        logger.info(f"{method} request to {url}")
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            attach_response(response.status_code, response.json(), headers=None)
            response.raise_for_status()
            logger.info(f"Status Code: {response.status_code}")
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                actual_json = response.json()
                attach_json("Response Body", actual_json)
                self.validate_response(actual_json=actual_json,expected_schema=expected_schema, schema_name=schema_name,auto_generate=auto_generate)
            else:
                logger.warning("Schema validation skipped. Reason: Response is not JSON.")
            return response
        
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout occurred while connecting to {url}: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error occurred (Status {response.status_code}): {e}")
            logger.error(f"Error Response Body: {response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection failed (DNS/Network down) for {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"An ambiguous error occurred while handling your request: {e}")
            raise

    def validate_response(self, actual_json, expected_schema, auto_generate,schema_name):
        if expected_schema is None and auto_generate and schema_name:
            expected_schema=self.generator.generate_schema(actual_json)
            attach_json("Generated Schema", expected_schema)
            logger.info(f"Generating baseline schema '{schema_name}'")
            self.generator.save_schema(expected_schema,schema_name)   
            logger.info(f"Baseline schema '{schema_name}' saved successfully")
        if  expected_schema is not None:
            validation_result = self.validator.validate_data(actual_json,expected_schema) 
            attach_schema_validation(validation_result)
            if not validation_result["missing"] and not validation_result["added"] and not validation_result["type_changes"]:
                logger.info("Schema validation passed")
            else:
                logger.warning(f"Schema validation failed: {validation_result}")
        else:
            logger.warning("Schema validation skipped. Reason: No schema provided.") 


    def get(self,endpoint, expected_schema=None,schema_name=None, auto_generate=False,**kwargs):
        return self.request("GET",endpoint,expected_schema=expected_schema,schema_name=schema_name,auto_generate=auto_generate,**kwargs)
    
    def post(self,endpoint,data=None,json=None,expected_schema=None,schema_name=None, auto_generate=False,**kwargs):
        return self.request("POST",endpoint,expected_schema=expected_schema,data=data,json=json,schema_name=schema_name,auto_generate=auto_generate,**kwargs)
    
    def delete(self,endpoint,expected_schema=None,schema_name=None, auto_generate=False,**kwargs):
        return self.request("DELETE",endpoint,expected_schema=expected_schema,schema_name=schema_name,auto_generate=auto_generate,**kwargs)
    
    def patch(self,endpoint,data=None,expected_schema=None,schema_name=None, auto_generate=False,**kwargs):
        return self.request("PATCH",endpoint,expected_schema=expected_schema,data=data,schema_name=schema_name,auto_generate=auto_generate,**kwargs)
    
    def put(self,endpoint,data=None,expected_schema=None,schema_name=None, auto_generate=False,**kwargs):
        return self.request("PUT",endpoint,expected_schema=expected_schema,data=data,schema_name=schema_name,auto_generate=auto_generate,**kwargs)
        

    