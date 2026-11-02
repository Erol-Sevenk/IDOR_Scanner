from dataclasses import dataclass
from scanner.core.sensitive_fields import extract_sensitive_values

@dataclass
class ContextAnalysisResult:
    sensitive_fields_found: dict
    belongs_to_attacker: bool   # degerler attacker'in kendi bilgisiyle eslesiyor mu
    belongs_to_victim: bool     # degerler owner'in bilgisiyle eslesiyor mu (asil tehlike)
    verdict: str                # "BOLA_CONFIRMED" / "LIKELY_SAFE" / "NEEDS_REVIEW"

def analyze_response_context(
    response_body: dict,
    attacker_known_values: set[str],   # orn. {"userB", "userb@test.com"}
    victim_known_values: set[str],     # orn. {"userA", "usera@test.com"}
) -> ContextAnalysisResult:
    sensitive = extract_sensitive_values(response_body)
    
    # Degerlerin hepsini string'e cevirip bir kume (set) yapiyoruz
    found_values = {str(v) for v in sensitive.values()}

    # Kesisim kumesi (intersection) ile bu degerler kime ait buluyoruz
    belongs_to_attacker = bool(found_values & attacker_known_values)
    belongs_to_victim = bool(found_values & victim_known_values)

    if belongs_to_victim and not belongs_to_attacker:
        verdict = "BOLA_CONFIRMED"      # baskasinin verisi dondu, saldirganin degil!
    elif belongs_to_attacker:
        verdict = "LIKELY_SAFE"         # donen veri zaten attacker'in kendi verisi
    elif sensitive:
        verdict = "NEEDS_REVIEW"        # hassas veri var ama kime ait belirsiz
    else:
        verdict = "LIKELY_SAFE"         # hic hassas veri yok

    return ContextAnalysisResult(
        sensitive_fields_found=sensitive,
        belongs_to_attacker=belongs_to_attacker,
        belongs_to_victim=belongs_to_victim,
        verdict=verdict,
    )

if __name__ == "__main__":
    # Gercek bulgunla test ediyoruz
    crapi_response = {
        "id": 6,
        "vehicle": {"owner": {"email": "user_tamir@test.com", "number": "2222222222"}},
    }

    result = analyze_response_context(
        response_body=crapi_response,
        attacker_known_values={"usera@test.com"},       # userA istegi atiyor (saldirgan)
        victim_known_values={"user_tamir@test.com"},    # user_tamir'in verisi geliyor (kurban)
    )

    print(f"Analiz Sonucu: {result.verdict}")
