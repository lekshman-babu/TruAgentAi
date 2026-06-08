import asyncio


async def send_message(lead_status : str)-> str:
    await asyncio.sleep(0.15) 

    if lead_status == "hot":
        return "Hello! I noticed you're interested in our product. Would you like to schedule a demo or have any questions I can help with?"
    elif lead_status == "warm":
        return "Hi there! I see you might be interested in our product. Can I provide you with more information or answer any questions you have?"
    else:
        return "Thank you for reaching out! If you have any questions about our product or need assistance, feel free to ask. I'm here to help!"