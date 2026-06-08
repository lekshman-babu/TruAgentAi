import json
import time


def load_context():
    try:
        with open("context.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def create_user_context(user_id):
    history = load_context()
    history[user_id] = {
        "context": {
            "contact_id": None,
            "lead_id": None,
            "last_interaction": None,
            "interactions": 0,
            "lead_score": 0,
            "last_message": None
        }
    }
    with open("context.json", "w") as f:
        json.dump(history, f)
    return history[user_id]


def retrieve_context(user_id):
    history = load_context()
    if user_id in history:
        return history[user_id]
    else:
        context = create_user_context(user_id)
        print("New user detected, Created context for " + user_id)
        return context


def store_context(user_id, retrieved_context, message):
    history = load_context()
    retrieved_context["context"]["last_interaction"] = time.time()
    retrieved_context["context"]["interactions"] = retrieved_context["context"].get("interactions", 0) + 1
    retrieved_context["context"]["last_message"] = message
    history[user_id] = retrieved_context
    with open("context.json", "w") as f:
        json.dump(history, f)
    return retrieved_context