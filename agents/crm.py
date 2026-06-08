import random
import asyncio


async def create_contact(retrieved_context : dict)-> int:
    await asyncio.sleep(0.15)

    if retrieved_context["context"]['contact_id'] is None:
        contact_id = random.randint(1000, 9999)
        retrieved_context["context"]['contact_id'] = contact_id
        return contact_id
    else:
        return retrieved_context["context"]['contact_id']