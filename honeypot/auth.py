API_KEY = "REPLACE_WITH_YOUR_API_KEY"

def validate_api_key(auth_header):
    if auth_header is None:
        return False
    try:
        parts = auth_header.strip().split(" ")
        if len(parts) != 2:
            return False
        scheme, token = parts
        if scheme.lower() != "bearer":
            return False
        return token == API_KEY
    except Exception:
        return False
