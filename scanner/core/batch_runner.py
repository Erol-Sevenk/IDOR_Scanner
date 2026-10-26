from scanner.models import Endpoint
from scanner.core.horizontal_bola import run_horizontal_bola_test

def run_batch(replayer, endpoints: list[Endpoint], owner_user: str, attacker_user: str):
    results = []
    for endpoint in endpoints:
        if not endpoint.id_parameters:
            continue

        # Path parametrelerini topla
        path_values = {
            p.name: p.example_value or "testA" if p.name == "username" else "1"
            for p in endpoint.id_parameters
            if p.location.value == "path"
        }
        
        # Query parametrelerini topla
        query_values = {
            p.name: p.example_value or "6"
            for p in endpoint.id_parameters
            if p.location.value == "query"
        }

        if not path_values and not query_values:
            continue

        try:
            result = run_horizontal_bola_test(
                replayer, endpoint, owner_user, attacker_user, path_values, query_values
            )
            results.append(result)
        except Exception as e:
            print(f"HATA ({endpoint.path}): {e}")

    return results
