import json
import redis
from loguru import logger

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Cache key constants
CACHE_ALL_USERS = "all_users"

# TTL constants
TTL_SHORT  = 30
TTL_MEDIUM = 60
TTL_LONG   = 300


def check_redis_connection() -> bool:
    try:
        redis_client.ping()
        logger.info("Redis connection successful")
        return True
    except Exception as e:
        logger.warning(f"Redis unavailable: {e}")
        return False


def get_cache(key: str):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        logger.warning(f"Redis GET error — key '{key}': {e}")
        return None


def set_cache(key: str, value, ttl: int = TTL_MEDIUM):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.warning(f"Redis SET error — key '{key}': {e}")


def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except Exception as e:
        logger.warning(f"Redis DELETE error — key '{key}': {e}")