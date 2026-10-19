from prance import ResolvingParser
from scanner.models import Endpoint

def read_openapi_spec(spec_path: str) -> list[Endpoint]:
    parser = ResolvingParser(spec_path)
    spec = parser.specification

    endpoints = []
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method.upper() not in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                continue
            endpoints.append(
                Endpoint(
                    path=path,
                    method=method.upper(),
                    source="openapi",
                )
            )
    return endpoints

if __name__ == "__main__":
    results = read_openapi_spec("targets/vampi_openapi.yaml")
    for ep in results:
        print(f"{ep.method:6} {ep.path}")
