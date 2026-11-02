import httpx
import yaml
from pydantic import BaseModel

class UserSession(BaseModel):
    username: str
    token: str
    raw_login_response: dict = {}

class SessionManager:
    def __init__(self, config_path: str, target_name: str):
        with open(config_path, "r", encoding="utf-8") as f:
            full_config = yaml.safe_load(f)
        self.config = full_config[target_name]
        self.base_url = self.config["base_url"]
        self.sessions: dict[str, UserSession] = {}

    def login_all(self) -> None:
        for user_key, creds in self.config["users"].items():
            response = httpx.post(f"{self.base_url}{self.config['login_endpoint']}", json=creds, timeout=10.0)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                kullanici = creds.get('email', creds.get('username'))
                print(f"\n[HATA] {user_key} ({kullanici}) icin giris basarisiz!")
                print(f"[HATA] HTTP Kodu: {e.response.status_code}")
                print(f"[HATA] crAPI Cevabi: {e.response.text}\n")
                raise
            data = response.json()
            self.sessions[user_key] = UserSession(
                username=creds.get("username", creds.get("email")),
                token=self._extract_token(data),
                raw_login_response=data,
            )

    def _extract_token(self, data: dict) -> str:
        field = self.config["token_field"]
        if field in data:
            return data[field]
        raise ValueError(f"Token field '{field}' not found in response: {data}")

    def get_token(self, user_key: str) -> str:
        return self.sessions[user_key].token

    def get_auth_header(self, user_key: str) -> dict:
        return {"Authorization": f"Bearer {self.get_token(user_key)}"}

    def get_known_identity_values(self, user_key: str) -> set[str]:
        session = self.sessions[user_key]
        values = {session.username}
        if "email" in session.raw_login_response:
            values.add(session.raw_login_response["email"])
        return values
