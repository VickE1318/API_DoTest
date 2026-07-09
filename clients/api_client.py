import requests
from utilities.logger import logging

class APIClient:
    def __init__(self,config):
        self.session = requests.Session()
        logging.INFO("Session Initiated")

    def request(self, method, endpoint, **kwargs):
        url = self.base_url + endpoint if endpoint[0] == '/' else url = self.base_url+"/"+endpoint
        logging.info(f"{method} request to {url}")
        response = self.session.request(method=method,url=url,**kwargs)
        logging.info(f"Status Code: {response.status_code}")
        return response
        

    