import time
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str):
    key = f"rate:{user_id}"
    now = time.time()

    # remove old entries
    window_start = now - 60
    r.zremrangebyscore(key, 0, window_start)

    # count
    count = r.zcard(key)

    if count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # add new request
    r.zadd(key, {str(now): now})
    r.expire(key, 60)