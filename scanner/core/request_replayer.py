import httpx
from scanner.models import Endpoint

class RequestReplayer:
    def __init__(self, base_url: str, session_manager):
        self.base_url = base_url
        self.sm = session_manager
        self.client = httpx.Client(timeout=10.0)

    def build_url(self, endpoint: Endpoint, path_values: dict) -> str:
        path = endpoint.path
        for key, value in path_values.items():
            path = path.replace(f"{{{key}}}", str(value))
        return f"{self.base_url}{path}"

    def build_url_with_query(self, endpoint: Endpoint, path_values: dict, query_values: dict) -> str:
        url = self.build_url(endpoint, path_values)
        if query_values:
            query_string = "&".join(f"{k}={v}" for k, v in query_values.items())
            url = f"{url}?{query_string}"
        return url

    def send_as_user(self, endpoint: Endpoint, user_key: str, path_values: dict = None, query_values: dict = None, body: dict = None) -> httpx.Response:
        path_values = path_values or {}
        query_values = query_values or {}
        
        url = self.build_url_with_query(endpoint, path_values, query_values)
        headers = self.sm.get_auth_header(user_key)

        response = self.client.request(
            method=endpoint.method,
            url=url,
            headers=headers,
            json=body if body else endpoint.body_example,
        )
        return response
