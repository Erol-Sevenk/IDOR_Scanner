from scanner.models import Endpoint
from scanner.core.session_manager import SessionManager
from scanner.core.request_replayer import RequestReplayer
from scanner.core.horizontal_bola import run_horizontal_bola_test

if __name__ == "__main__":
    print("[*] VAmPI oturumlari aciliyor...")
    sm = SessionManager("config/users.yaml", "vampi")
    sm.login_all()
    replayer = RequestReplayer("http://localhost:5000", sm)
    
    endpoint = Endpoint(path="/users/v1/{username}", method="GET", source="manual")
    
    print("\n[*] GERCEK SISTEM NEGATIF KONTROL TESTI (VAmPI)")
    print("    Senaryo: userA kendi profiline bakiyor (Zafiyet OLMAMALI)")
    
    # Saldirgan da Kurban da Ayni Kisi!
    result = run_horizontal_bola_test(
        replayer=replayer,
        endpoint=endpoint,
        owner_user="userA",
        attacker_user="userA",
        attacker_known_values=sm.get_known_identity_values("userA"),
        victim_known_values=sm.get_known_identity_values("userA"),
        path_values={"username": "testA"}
    )
    
    print(f"\nHTTP Status: {result.status_code}")
    print(f"Motor Karari: {result.verdict}")
    print(f"Tespit Edilen Hassas Veriler: {list(result.sensitive_fields.keys())}")
