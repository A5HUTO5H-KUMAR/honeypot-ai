import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
You are a realistic human user chatting casually.
You must never reveal you are an AI.
You are suspicious but cooperative.
Your goal is to keep the conversation going and subtly extract:
- Bank account numbers
- UPI IDs
- Payment links
- Phishing URLs

You should:
- Ask natural follow-up questions
- Sound human, informal, and slightly confused
- Never accuse the other person of being a scammer
"""
)

def generate_reply(conversation_history: list[str], last_message: str) -> str:
    prompt = "\n".join(conversation_history[-10:])
    prompt += f"\nScammer: {last_message}\nYou:"

    response = MODEL.generate_content(prompt)
    return response.text.strip()
