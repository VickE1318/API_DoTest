import json
import allure
from allure_commons.types import AttachmentType


def attach_json(name, data):
    allure.attach(
        json.dumps(data, indent=4),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

def attach_request(method, url, headers=None, payload=None):
    request_details = {
        "Method": method,
        "URL": url,
        "Headers": headers or {},
        "Payload": payload or {}
    }
    attach_json("API Request Details", request_details)

def attach_response(status_code, body, headers=None):
    response_details = {
        "Status Code": status_code,
        "Headers": dict(headers) if headers else {},
        "Response Body": body
    }
    attach_json("API Response Details", response_details)

def attach_schema_validation(result):
    summary = {
        "Validation Status": "PASSED" if not result.get("missing") and not result.get("added") and not result.get("type_changes") else "FAILED",
        "Details": result
    }
    attach_json("Schema Validation Result", summary)