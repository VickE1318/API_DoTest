import pytest
from utilities.config_loader import load_config
from utilities.logger import setup_logger
from clients.api_client import APIClient

@pytest.fixture(scope="session")
def config():
    config_obj=load_config("config/config.yaml")
    return config_obj

@pytest.fixture(scope="session")
def api_client(config):
    current_env = config["environment"]
    base_url=config["environments"][current_env]["base_url"]
    client_obj = APIClient(base_url)
    return client_obj

@pytest.fixture(scope="session",autouse=True)
def logger():
    setup_logger()
