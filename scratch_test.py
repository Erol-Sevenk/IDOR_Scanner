from deepdiff import DeepDiff
import pprint

baseline = {"id": 1, "username": "userA", "email": "usera@test.com"}
test = {"id": 1, "username": "userA", "email": "usera@test.com"}  # aynı

print("--- Ayni Veri Testi ---")
pprint.pprint(DeepDiff(baseline, test))  # boş {} dönmeli

test2 = {"message": "Forbidden"}  # farklı yapı
print("\n--- Farkli Veri Testi ---")
pprint.pprint(DeepDiff(baseline, test2))  # fark dönmeli
