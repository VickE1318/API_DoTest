import requests
from utilities.logger import logging

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    def request(self, method, endpoint, **kwargs):
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = self.base_url + endpoint
        logging.info(f"{method} request to {url}")
        try:
            response = self.session.request(method=method, url=url, timeout=10, **kwargs)
            response.raise_for_status()
            logging.info(f"Status Code: {response.status_code}")
            return response
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout occurred while connecting to {url}: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error occurred (Status {response.status_code}): {e}")
            logging.error(f"Error Response Body: {response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Network connection failed (DNS/Network down) for {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"An ambiguous error occurred while handling your request: {e}")
            raise
    def get_req(self,endpoint,**kwargs):
        return self.request("GET",endpoint,**kwargs)
    def post_req(self,endpoint,data,json,**kwargs):
        return self.request("POST",endpoint,data=data,json=json,**kwargs)
    def delete_req(self,endpoint,**kwargs):
        return self.request("DELETE",endpoint,**kwargs)
    def patch_req(self,endpoint,data,**kwargs):
        return self.request("PATCH",endpoint,data=data,**kwargs)
    def put_req(self,endpoint,data,**kwargs):
        return self.request("PUT",endpoint,data=data,**kwargs)
        

    