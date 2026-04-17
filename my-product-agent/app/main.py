from fastapi import FastAPI, Depends
import redis
import json
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

from utils.mock_llm import ask, ask_stream

class AskRequest(BaseModel):
    question: str

app = FastAPI()

r = redis.from_url(settings.REDIS_URL, decode_responses=True)


# =========================
# Health
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# Readiness (check Redis)
# =========================
@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}


# =========================
# Main endpoint
# =========================
@app.post("/ask")
def ask_api(
    req: AskRequest,
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget)
):
    question = req.question
    key = f"history:{user_id}"

    # 1. Load history
    history_raw = r.get(key)
    history = json.loads(history_raw) if history_raw else []

    # 2. Call mock LLM
    answer = ask(question)

    # 3. Save history
    history.append({
        "question": question,
        "answer": answer
    })

    r.set(key, json.dumps(history), ex=3600)

    # 4. Return
    return {
        "answer": answer,
        "history_length": len(history)
    }

@app.get("/ask-stream")
def ask_stream_api(question: str):
    def generator():
        for chunk in ask_stream(question):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")