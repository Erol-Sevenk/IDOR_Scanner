from scanner.core.context_analyzer import analyze_response_context

test_cases = [
    {
        "name": "VAmPI - userB userA profiline erisiyor",
        "response": {"username": "userA", "email": "usera@test.com"},
        "attacker_known": {"userb@test.com", "testB"},
        "victim_known": {"usera@test.com", "testA"},
        "expected": "BOLA_CONFIRMED",
    },
    {
        "name": "crAPI - userA userB'nin mechanic raporuna erisiyor",
        "response": {"vehicle": {"owner": {"email": "tamirci@test.com"}}},
        "attacker_known": {"usera@test.com"},
        "victim_known": {"tamirci@test.com"},
        "expected": "BOLA_CONFIRMED",
    },
    {
        "name": "Negatif kontrol - kendi verisine erisim (Guvenli)",
        "response": {"username": "userA", "email": "usera@test.com"},
        "attacker_known": {"usera@test.com", "testA"},
        "victim_known": {"usera@test.com", "testA"},
        "expected": "LIKELY_SAFE",
    },
]

print("[*] Yeni Analiz Motoru Dogrulama Testleri Basliyor...\n")
for case in test_cases:
    result = analyze_response_context(case["response"], case["attacker_known"], case["victim_known"])
    status = "✅" if result.verdict == case["expected"] else "❌"
    print(f"{status} {case['name']}")
    print(f"    Beklenen: {case['expected']} | Gelen: {result.verdict}\n")
