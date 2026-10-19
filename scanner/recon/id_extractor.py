import re
from scanner.models import Endpoint, IDParameter, ParamLocation

ID_NAME_PATTERNS = [
    r"^id$", r"_id$", r"^id_", 
    r"uuid", r"guid",
    r"username", r"user_name",
    r"report_id", r"order_id", r"vehicle_id", r"post_id",
]

def extract_path_id_params(endpoint: Endpoint) -> list[IDParameter]:
    found = []
    path_vars = re.findall(r"\{(\w+)\}", endpoint.path)
    for var in path_vars:
        confidence = 0.9 if any(re.search(p, var, re.IGNORECASE) for p in ID_NAME_PATTERNS) else 0.5
        found.append(IDParameter(name=var, location=ParamLocation.PATH, confidence=confidence))
    return found

def extract_body_id_params(body: dict | None) -> list[IDParameter]:
    found = []
    if not body:
        return found
    for key, value in body.items():
        if any(re.search(p, key, re.IGNORECASE) for p in ID_NAME_PATTERNS):
            found.append(IDParameter(name=key, location=ParamLocation.BODY, confidence=0.8, example_value=str(value)))
    return found

def enrich_endpoint_with_id_params(endpoint: Endpoint) -> Endpoint:
    endpoint.id_parameters = extract_path_id_params(endpoint)
    if endpoint.body_example:
        endpoint.id_parameters += extract_body_id_params(endpoint.body_example)
    return endpoint
