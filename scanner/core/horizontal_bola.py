from dataclasses import dataclass
from scanner.models import Endpoint
from scanner.core.request_replayer import RequestReplayer

@dataclass
class BolaTestResult:
    endpoint: str
    method: str
    owner_user: str
    attacker_user: str
    status_code: int
    response_body: str
    suspicious: bool

def run_horizontal_bola_test(
    replayer: RequestReplayer,
    endpoint: Endpoint,
    owner_user: str,
    attacker_user: str,
    path_values: dict = None,
    query_values: dict = None,
) -> BolaTestResult:
    
    response = replayer.send_as_user(
        endpoint, attacker_user, path_values=path_values, query_values=query_values
    )
    
    suspicious = response.status_code in (200, 201, 204)
    
    return BolaTestResult(
        endpoint=endpoint.path,
        method=endpoint.method,
        owner_user=owner_user,
        attacker_user=attacker_user,
        status_code=response.status_code,
        response_body=response.text[:500],
        suspicious=suspicious,
    )
