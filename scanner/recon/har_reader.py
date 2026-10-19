import json
import re
from urllib.parse import urlparse
from scanner.models import Endpoint

def normalize_path(path: str) -> str:
    path = re.sub(r"/\d+(?=/|$)", "/{id}", path)
    path = re.sub(
        r"/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?=/|$)",
        "/{uuid}",
        path,
    )
    # crAPI alfanümerik ID'lerini (örneğin 20+ karakterli) {id} yap
    path = re.sub(r"/[a-zA-Z0-9]{20,}(?=/|$)", "/{id}", path)
    return path

def read_har_file(har_path: str, base_host: str = "localhost:8888") -> list[Endpoint]:
    with open(har_path, "r", encoding="utf-8") as f:
        har = json.load(f)

    seen = set()
    endpoints = []

    for entry in har["log"]["entries"]:
        request = entry["request"]
        url = urlparse(request["url"])

        if base_host not in url.netloc:
            continue
        if not url.path.startswith(("/users", "/books", "/identity", "/workshop", "/community")):
            continue

        method = request["method"]
        path = normalize_path(url.path)

        key = f"{method} {path}"
        if key in seen:
            continue
        seen.add(key)

        headers = {h["name"]: h["value"] for h in request.get("headers", [])
                   if h["name"].lower() == "authorization"}

        body_example = None
        if "postData" in request:
            try:
                body_example = json.loads(request["postData"]["text"])
            except (KeyError, json.JSONDecodeError):
                pass

        endpoints.append(
            Endpoint(
                path=path,
                method=method,
                source="har",
                raw_headers=headers,
                body_example=body_example,
            )
        )
    return endpoints
