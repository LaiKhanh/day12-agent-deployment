import redis
from fastapi import HTTPException
from datetime import datetime
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

COST_PER_REQUEST = 0.01

def check_budget(user_id: str):
    month = datetime.now().strftime("%Y-%m")
    key = f"cost:{user_id}:{month}"

    current = r.get(key)
    total = float(current) if current else 0

    if total + COST_PER_REQUEST > settings.MONTHLY_BUDGET_USD:
        raise HTTPException(status_code=402, detail="Budget exceeded")

    r.incrbyfloat(key, COST_PER_REQUEST)