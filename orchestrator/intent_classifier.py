import os
from google import genai
from google.genai import types
from dotenv import load_dotenv  # ← add this


SALES_KEYWORDS = {
    "pricing", "price", "cost", "quote", "plan", "plans", "buy", "purchase",
    "demo", "trial", "subscription", "seats", "users", "license", "licenses",
    "enterprise", "upgrade", "sales", "budget",
}

SUPPORT_KEYWORDS = {
    "issue", "problem", "error", "bug", "broken", "can't", "cannot", "cant",
    "help", "support", "account", "login", "password", "reset", "not working",
    "fail", "failed", "crash", "refund", "cancel", "complaint",
}

load_dotenv() 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def intent(message : str)-> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Classify the user's message as exactly one of: "
                    "sales or support. "
                    "Reply with only that label and nothing else."
                ),
                max_output_tokens=10,
            ),
        )
        label = response.text.strip().lower()
        print("Classified form Gemini")
    except Exception as e:
        print(f"Error occurred: {e}")
        label = ""   # network/key problem -> fall back to rules below

    # Trust the model only if it gave us a clean, expected label.
    if "support" in label:
        return "support"
    elif "sales" in label:
        return "sales"
    else:
        msg = (message or "").lower()
        sales = sum(1 for w in SALES_KEYWORDS if w in msg)
        support = sum(1 for w in SUPPORT_KEYWORDS if w in msg)
        if support > sales:
            return "support"
        return "sales"