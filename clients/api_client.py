import requests
from utilities.logger import get_logger
from validators.schema_validator import SchemaValidator
logger = get_logger()

class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.validator = SchemaValidator()

    def request(self, method, endpoint, expected_schema=None, **kwargs):
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = self.base_url + endpoint
        logger.info(f"{method} request to {url}")
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            logger.info(f"Status Code: {response.status_code}")
            content_type = response.headers.get("Content-Type", "")
            if expected_schema:
                if "application/json" in content_type:
                    actual_json = response.json()
                    validation_result = self.validator.validate_data(actual_json,expected_schema) 
                    if not validation_result["missing"] and not validation_result["added"] and not validation_result["type_changes"]:
                        logger.info("Schema validation passed")
                    else:
                        logger.warning(f"Schema validation failed: {validation_result}")
                else:
                    logger.warning("Schema validation skipped. Reason: Response is not JSON.")
            else:
                logger.warning("Schema validation skipped. Reason: No schema provided.")
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

    def get(self,endpoint, expected_schema=None,**kwargs):
        return self.request("GET",endpoint,expected_schema=expected_schema,**kwargs)
    
    def post(self,endpoint,data=None,json=None,expected_schema=None,**kwargs):
        return self.request("POST",endpoint,expected_schema=expected_schema,data=data,json=json,**kwargs)
    
    def delete(self,endpoint,expected_schema=None,**kwargs):
        return self.request("DELETE",endpoint,expected_schema=expected_schema,**kwargs)
    
    def patch(self,endpoint,data=None,expected_schema=None,**kwargs):
        return self.request("PATCH",endpoint,expected_schema=expected_schema,data=data,**kwargs)
    
    def put(self,endpoint,data=None,expected_schema=None,**kwargs):
        return self.request("PUT",endpoint,expected_schema=expected_schema,data=data,**kwargs)
        

    