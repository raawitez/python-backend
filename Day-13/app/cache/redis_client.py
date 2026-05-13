import json
import redis 
from loguru import logger

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_response = True
)

def check_redis_connection():
    try:
        redis_client.ping()
        logger.info("Redis connection successful")
        return True
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        return False
    
def get_cache(key: str):
    try:
        value = redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)
    
    except Exception as e:
        logger.warning(f"Redis GET failed for key '{key}': {e}")
        return None
    
def set_cache(key: str, value, ttl: int = 60):
    try:
        json_value = json.dumps(value)
        redis_client.setex(key, ttl, json_value)
        logger.debug(f"Cache SET: '{key}' (TTL: {ttl}s)")
    except Exception as e:
        logger.warning(f"Redis SET failed for key '{key}': {e}")

def delete_cache(key: str):
    try:
        redis_client.delete(key)
        logger.debug(f"Cache DELETE: '{key}'")
    except Exception as e:
        logger.warning(f"Redis DELETE failed for key '{key}': {e}")

def delete_pattern(pattern: str):
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            logger.debug(f"Cache cleared pattern: '{pattern}' ({len(keys)} keys)")
    except Exception as e:
        logger.warning(f"Redis pattern delete failed: {e}")

CACHE_ALL_USERS = "all_users"
CACHE_USER = "user:{user_id}"

TTL_SHORT = 30
TTL_MEDIUM = 60
TTL_LONG = 300