# TruAgent — Multi-Agent Orchestrator (MVP)

A hub-based AI orchestrator that classifies user intent, routes the request to the right agents, and executes a multi-agent workflow.

**Flow:** Input → Intent Classification → Routing → Agent Execution → Response

## Setup & Run

```bash
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

## Testing the two scenarios

In `http://localhost:8000/docs` → `POST /agent/run` → **Try it out** → paste a body → **Execute**.

**Scenario 1 — sales (full pipeline):**

```json
{"message":"I need pricing for 500 users","context":{"source":"chat","user_id":"user-123"}}
```

**Scenario 2 — support (single agent):**

```json
{"message":"I have an issue with my account","context":{"source":"chat","user_id":"user-456"}}
```


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
