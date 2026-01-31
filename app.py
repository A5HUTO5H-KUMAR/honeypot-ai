from agent import generate_reply
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time

from auth import validate_api_key
from scam_detector import detect_scam
from memory import get_conversation
from extractor import extract_intelligence

app = FastAPI()

# Optional but safe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

class HoneypotRequest(BaseModel):
    conversation_id: str = "default"
    message: str = ""

@app.post("/honeypot")
def honeypot(payload: HoneypotRequest, authorization: str = Header(None)):
    if not validate_api_key(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")

    start = time.time()

    scam_result = detect_scam(payload.message)
    memory = get_conversation(payload.conversation_id)

    agent_reply = None

    if scam_result["is_scam"]:
        # Update memory
        memory["turns"] += 1
        memory["messages"].append(f"Scammer: {payload.message}")

        # Extract intelligence
        extract_intelligence(payload.message, memory)

        # 🔥 GENERATE AI AGENT RESPONSE
        agent_reply = generate_reply(
            conversation_history=memory["messages"],
            last_message=payload.message
        )

        # Store agent reply
        memory["messages"].append(f"Agent: {agent_reply}")

    engagement_duration = round(time.time() - memory["start_time"], 2)

    return {
        "scam_detected": scam_result["is_scam"],
        "confidence_score": scam_result["confidence"],
        "agent_engaged": scam_result["is_scam"],
        "agent_reply": agent_reply,  # ⭐ VERY IMPORTANT
        "conversation_metrics": {
            "turns": memory["turns"],
            "engagement_duration": f"{engagement_duration}s"
        },
        "extracted_intelligence": {
            "bank_account": memory["entities"]["bank_account"],
            "upi_id": memory["entities"]["upi_id"],
            "phishing_links": memory["entities"]["phishing_links"]
        }
    }
