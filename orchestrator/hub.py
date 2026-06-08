from orchestrator.workflow import get_workflow
from agents.base import base_agent
from orchestrator.intent_classifier import intent
from orchestrator.context_handler import retrieve_context, store_context


def user_intent(message : dict)-> str:
    return intent(message['message'])


def workflow(intent : str)-> list:
    return get_workflow(intent)


async def agent_router(message : dict)-> dict:
    intent = user_intent(message)

    if intent == "sales":
        workflow(intent)   # builds + prints the sales_pipeline visualization
        agents_involved = ["crm", "lead", "chat", "notify"]
        reason = "Detected a sales intent, so the multi-agent sales_pipeline is triggered."
    else:
        agents_involved = ["support"]
        reason = "Detected a support intent, so the request is routed to the support agent only."

    retrieved_context = retrieve_context(message["context"]['user_id'])

    result = await base_agent(message, retrieved_context, intent)

    store_context(message["context"]['user_id'], retrieved_context, message["message"])

    return {
        "intent": intent,
        "routing": {
            "agents": agents_involved,
            "reason": reason,
        },
        "steps": result["steps"],
        "context": retrieved_context["context"],
    }