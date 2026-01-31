import re

def extract_intelligence(message, memory):
    if not isinstance(message, str):
        return

    # Bank account: 10–18 digits, not starting with 000
    bank_matches = re.findall(r"\b\d{10,18}\b", message)
    if bank_matches and memory["entities"]["bank_account"] is None:
        candidate = bank_matches[0]
        if not candidate.startswith("000"):
            memory["entities"]["bank_account"] = candidate

    # Strict UPI IDs only
    upi_matches = re.findall(
        r"\b[a-zA-Z0-9.\-_]{2,}@(upi|okaxis|oksbi|okhdfc|paytm|ibl)\b",
        message.lower()
    )
    if upi_matches and memory["entities"]["upi_id"] is None:
        memory["entities"]["upi_id"] = upi_matches[0]

    # Phishing links
    links = re.findall(r"https?://[^\s]+", message)
    for link in links:
        if link not in memory["entities"]["phishing_links"]:
            memory["entities"]["phishing_links"].append(link)
