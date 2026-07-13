import pytest
from utilities.config_loader import load_config
from utilities.logger import setup_logger
from clients.api_client import APIClient

@pytest.fixture(scope="session")
def config_caller():
    config=load_config("config/config.yaml")
    return config

@pytest.fixture(scope="session")
def log_caller():
    logger=setup_logger()
    return logger

@pytest.fixture(scope="session")
def client_caller():
    client_obj = APIClient.request()
    return client_obj
