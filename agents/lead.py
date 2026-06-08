import re
import random
import asyncio


def score_lead(message : str, retrieved_context : dict)-> int:

    msg = (message or "").lower()
    score = 30  # baseline for any inbound sales touch


    match = re.search(r"(\d[\d,]*)\s*(users|people|employees|licenses)",msg)
    if not match:
        match = re.search(r"\b(\d{2,})\b", msg) 
    if match:
        users = int(match.group(1).replace(",", ""))
        if users >= 1000:
            score += 50
        elif users >= 500:
            score += 40
        elif users >= 100:
            score += 25
        elif users >= 10:
            score += 15

    for kw, pts in (("pricing", 15), ("quote", 15), ("demo", 10),
                    ("buy", 20), ("enterprise", 10), ("budget", 10)):
        if kw in msg:
            score += pts

    return min(score, 100)


async def create_lead(message : dict, retrieved_context : dict)-> str:
    await asyncio.sleep(0.15)   # mock work

    if retrieved_context["context"]['lead_id'] is None:
        retrieved_context["context"]['lead_id'] = random.randint(1000, 9999)

    score = score_lead(message["message"], retrieved_context)
    retrieved_context["context"]['lead_score'] = score

    if score > 70:
        return "hot"
    elif score > 40:
        return "warm"
    else:
        return "cold"