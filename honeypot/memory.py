import time

conversation_store = {}

def get_conversation(conversation_id):
    if not isinstance(conversation_id, str) or conversation_id.strip() == "":
        conversation_id = "default"

    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = {
            "turns": 0,
            "start_time": time.time(),
            "entities": {
                "bank_account": None,
                "upi_id": None,
                "phishing_links": []
            }
        }
    return conversation_store[conversation_id]
