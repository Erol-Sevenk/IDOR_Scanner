from scanner.recon.openapi_reader import read_openapi_spec
from scanner.recon.har_reader import read_har_file
from scanner.recon.id_extractor import enrich_endpoint_with_id_params
import json

if __name__ == "__main__":
    vampi_endpoints = [enrich_endpoint_with_id_params(e) for e in read_openapi_spec("targets/vampi_openapi.yaml")]
    crapi_endpoints = [enrich_endpoint_with_id_params(e) for e in read_har_file("targets/crapi_session.har")]
    
    all_endpoints = vampi_endpoints + crapi_endpoints
    
    for ep in all_endpoints:
        if ep.id_parameters:
            print(f"{ep.method:6} {ep.path:50} -> ID params: {[p.name for p in ep.id_parameters]}")
    
    with open("targets/discovered_endpoints.json", "w") as f:
        json.dump([e.model_dump() for e in all_endpoints], f, indent=2)
    
    print(f"\n[+] Toplam {len(all_endpoints)} endpoint analiz edildi ve targets/discovered_endpoints.json dosyasina kaydedildi.")
