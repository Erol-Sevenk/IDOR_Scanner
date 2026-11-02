from dataclasses import dataclass
from scanner.models import Endpoint
from scanner.core.request_replayer import RequestReplayer
from scanner.core.context_analyzer import analyze_response_context

@dataclass
class BolaTestResult:
    endpoint: str
    method: str
    owner_user: str
    attacker_user: str
    status_code: int
    verdict: str
    sensitive_fields: dict
    reason: str

def run_horizontal_bola_test(
    replayer: RequestReplayer,
    endpoint: Endpoint,
    owner_user: str,
    attacker_user: str,
    attacker_known_values: set[str],
    victim_known_values: set[str],
    path_values: dict = None,
    query_values: dict = None,
) -> BolaTestResult:
    
    response = replayer.send_as_user(
        endpoint, attacker_user, path_values=path_values, query_values=query_values
    )
    
    if response.status_code not in (200, 201, 204):
        return BolaTestResult(
            endpoint=endpoint.path, method=endpoint.method,
            owner_user=owner_user, attacker_user=attacker_user,
            status_code=response.status_code, verdict="LIKELY_SAFE",
            sensitive_fields={}, reason=f"HTTP Status = {response.status_code}"
        )
        
    try:
        body = response.json()
    except ValueError:
         return BolaTestResult(
            endpoint=endpoint.path, method=endpoint.method,
            owner_user=owner_user, attacker_user=attacker_user,
            status_code=response.status_code, verdict="NEEDS_REVIEW",
            sensitive_fields={}, reason="JSON olmayan yanit"
        )
        
    analysis = analyze_response_context(body, attacker_known_values, victim_known_values)
    
    return BolaTestResult(
        endpoint=endpoint.path, method=endpoint.method,
        owner_user=owner_user, attacker_user=attacker_user,
        status_code=response.status_code, verdict=analysis.verdict,
        sensitive_fields=analysis.sensitive_fields_found, reason="Icerik analizi yapildi"
    )
