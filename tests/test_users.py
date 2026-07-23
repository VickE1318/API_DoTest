import allure
import json

wrong_schema = {
    "id": "str",
    "name": "int"
}


@allure.feature("Users API")
@allure.story("GET User")
@allure.title("Verify GET User")
def test_get_user(api_client):
    response = api_client.get(
        "/users/1",
        schema_name="user",
        auto_generate=True
    )
    assert response.status_code == 200