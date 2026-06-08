import asyncio


async def notify_team(lead_status : str, contact_id : int)-> dict:
    await asyncio.sleep(0.15)   # mock work

    channel = "sale-hot" if lead_status == "hot" else "sale-warm"
    return {
        "channel": channel,
        "message": f"New priority lead with contact ID {contact_id} and status {lead_status}"
    }