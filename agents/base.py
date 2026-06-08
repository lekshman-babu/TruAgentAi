import asyncio
from agents.chat import send_message
from agents.crm import create_contact
from agents.notification import notify_team
from agents.lead import create_lead


async def base_agent(message : dict, retrieved_context : dict, intent : str)-> dict:
    if intent == "sales":
        steps = []

        contact_id = await create_contact(retrieved_context)
        steps.append({"agent": "crm", "status": "done", "output": contact_id})

        lead_status = await create_lead(message, retrieved_context)
        lead_score = retrieved_context["context"]['lead_score']
        steps.append({"agent": "lead", "status": "done",
                      "output": {"status": lead_status, "score": lead_score}})

        if lead_status in ["hot", "warm"]:
            notify_result, chat_result = await asyncio.gather(
                notify_team(lead_status, contact_id),
                send_message(lead_status)
            )
            steps.append({"agent": "chat", "status": "done", "output": chat_result})
            steps.append({"agent": "notify", "status": "done", "output": notify_result})
        else:
            chat_result = await send_message(lead_status)
            steps.append({"agent": "chat", "status": "done", "output": chat_result})

        return {
            "workflow": "sales_pipeline",
            "steps": steps,
        }

    elif intent == "support":
        reply = "Thank you for reaching out to support. A support agent will be with you shortly to assist you with your issue."
        return {
            "steps": [{"agent": "support", "status": "done", "output": reply}],
        }