SENSITIVE_FIELD_PATTERNS = [
    "email", "e_mail", "e-posta",
    "password", "password_hash", "secret", "token",
    "phone", "number", "telefon",
    "address", "adres",
    "tc_no", "tc_kimlik", "national_id",
    "balance", "bakiye",
    "vin",                      # crAPI'ye ozel
    "name", "first_name", "last_name", "isim",
]

def is_sensitive_field(field_name: str) -> bool:
    field_lower = field_name.lower()
    return any(pattern in field_lower for pattern in SENSITIVE_FIELD_PATTERNS)

def extract_sensitive_values(data, path: str = "") -> dict:
    """
    Ic ice JSON'da hassas alanlari ve degerlerini bulur.
    Doner: {"vehicle.owner.email": "usera@test.com", ...}
    """
    found = {}

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if is_sensitive_field(key) and not isinstance(value, (dict, list)):
                found[current_path] = value
            elif isinstance(value, (dict, list)):
                found.update(extract_sensitive_values(value, current_path))

    elif isinstance(data, list):
        for i, item in enumerate(data):
            found.update(extract_sensitive_values(item, f"{path}[{i}]"))

    return found

if __name__ == "__main__":
    sample_response = {
        "id": 6,
        "vehicle": {
            "id": 102,
            "vin": "PN38331F5W59GL656",
            "owner": {"email": "user_tamir@test.com", "number": "2222222222"}
        },
        "problem_details": "eweew",
    }
    result = extract_sensitive_values(sample_response)
    print("Bulunan Hassas Alanlar:")
    import pprint
    pprint.pprint(result)
