from fastapi import FastAPI
from orchestrator.hub import agent_router

app = FastAPI(title="TruAgent")


@app.post("/agent/run")
async def agent_run(payload: dict):
    return await agent_router(payload)