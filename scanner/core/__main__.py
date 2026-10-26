import json
from scanner.models import Endpoint
from scanner.core.session_manager import SessionManager
from scanner.core.request_replayer import RequestReplayer
from scanner.core.batch_runner import run_batch

if __name__ == "__main__":
    print("[*] Sistem hazirlaniyor: VAmPI ve crAPI oturumlari aciliyor...")
    
    # 1. VAmPI Oturumu
    sm_vampi = SessionManager("config/users.yaml", "vampi")
    sm_vampi.login_all()
    replayer_vampi = RequestReplayer("http://localhost:5000", sm_vampi)
    
    # 2. crAPI Oturumu
    sm_crapi = SessionManager("config/users.yaml", "crapi")
    sm_crapi.login_all()
    replayer_crapi = RequestReplayer("http://localhost:8888", sm_crapi)
    
    # 3. Endpointleri Oku
    with open("targets/discovered_endpoints.json", "r", encoding="utf-8") as f:
        raw_endpoints = json.load(f)
    all_endpoints = [Endpoint(**raw) for raw in raw_endpoints]
    
    # Hedefleri ayir (URL yollarina gore)
    vampi_endpoints = [e for e in all_endpoints if e.path.startswith(("/users", "/books"))]
    crapi_endpoints = [e for e in all_endpoints if e.path.startswith(("/identity", "/workshop", "/community"))]
    
    print("\n[*] YATAY BOLA TOPLU TARAMASI BASLIYOR...\n")
    
    print("--- VAmPI Sonuclari ---")
    vampi_results = run_batch(replayer_vampi, vampi_endpoints, 'userA', 'userB')
    for r in vampi_results:
        flag = '🚨' if r.suspicious else '✅'
        print(f"{flag} {r.method:6} {r.endpoint:40} -> HTTP {r.status_code}")
        
    print("\n--- crAPI Sonuclari ---")
    crapi_results = run_batch(replayer_crapi, crapi_endpoints, 'userA', 'userB')
    for r in crapi_results:
        flag = '🚨' if r.suspicious else '✅'
        print(f"{flag} {r.method:6} {r.endpoint:40} -> HTTP {r.status_code}")

    print(f"\n[+] Tarama tamamlandi! Toplam test edilen ID'li endpoint: {len(vampi_results) + len(crapi_results)}")
