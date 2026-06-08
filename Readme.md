# TruAgent — Multi-Agent Orchestrator (MVP)

A hub-based AI orchestrator that classifies user intent, routes the request to the right agents, and executes a multi-agent workflow.

**Flow:** Input → Intent Classification → Routing → Agent Execution → Response

## Setup & Run

```bash
# from the project root (TruAgent AI)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.app:app --reload
```

Then open the interactive API docs:

```
http://localhost:8000/docs
```

### API key (optional but recommended)

Intent classification uses **Gemini with a rule-based fallback**. To use the LLM path, create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

If no key is set, the system still runs — it automatically falls back to keyword-based intent classification.

> `.env` is gitignored and must never be committed.

## Testing the two scenarios

In `http://localhost:8000/docs` → `POST /agent/run` → **Try it out** → paste a body → **Execute**.

**Scenario 1 — sales (full pipeline):**

```json
{"message":"I need pricing for 500 users","context":{"source":"chat","userId":"user-123"}}
```

Expected: `intent: "sales"`, lead score 85 (hot), all four agents (CRM, Lead, Chat, Notify) return `done`.

**Scenario 2 — support (single agent):**

```json
{"message":"I have an issue with my account","context":{"source":"chat","userId":"user-456"}}
```

Expected: `intent: "support"`, routed to a single support agent.

## Project Structure

```
TruAgent/
├── api/
│   └── app.py                 # FastAPI endpoint: POST /agent/run
├── orchestrator/
│   ├── hub.py                 # central hub: intent → route → execute → store
│   ├── intent_classifier.py   # Gemini intent classification + rule-based fallback
│   ├── workflow.py            # sales_pipeline declaration + visualization
│   └── context_handler.py     # per-user memory (context.json)
├── agents/
│   ├── base.py                # executes the agent workflow
│   ├── crm.py                 # create_contact
│   ├── lead.py                # create_lead + scoring
│   ├── chat.py                # send_message
│   └── notification.py        # notify_team
├── requirements.txt
└── README.md
```

## Documentation

See the design doc for the architecture overview, how orchestration works, and limitations.

## Notes

- `context.json` is created automatically on first run; it stores per-user memory and can be deleted to reset state.
- `.env` and `context.json` are gitignored.
