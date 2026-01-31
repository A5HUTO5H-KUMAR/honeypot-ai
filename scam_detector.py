import re

KEYWORDS = {
    "urgency": ["urgent", "immediately", "now"],
    "threat": ["blocked", "suspended", "locked"],
    "finance": ["bank", "account", "upi", "payment"]
}

def detect_scam(message):
    if not isinstance(message, str) or message.strip() == "":
        return {"is_scam": False, "confidence": 0.0}

    text = message.lower()
    score = 0

    for words in KEYWORDS.values():
        for w in words:
            if w in text:
                score += 1
                break

    if re.search(r"https?://", text):
        score += 2

    confidence = min(score / 5, 1.0)
    confidence = max(0.0, round(confidence, 2))

    return {
        "is_scam": confidence >= 0.5,
        "confidence": confidence
    }
