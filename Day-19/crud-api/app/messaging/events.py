QUEUE_USER_EVENTS = "user_events"
QUEUE_NOTIFICATIONS = "notifications"

EVENT_USER_REGISTERED = "user_registered"
EVENT_USER_UPDATED    = "user_updated"
EVENT_USER_DELETED    = "user_deleted"
EVENT_USER_LOGIN      = "user_login"

from datetime import datetime

def build_user_registered_event(user_id:int, email:str, name:str)->dict:
    return{
        "event": EVENT_USER_REGISTERED,
        "user_id": user_id,
        "email": email,
        "name": name,
        "timestamp": datetime.utcnow().isoformat()
    }

def build_user_updated_event(user_id: int, changes:dict)->dict:
    return{
        "event": EVENT_USER_UPDATED,
        "user_id": user_id,
        "changes": changes,
        "timestamp": datetime.utcnow().isoformat()
    }

def build_user_deleted_event(user_id: int, email:str, name:str)->dict:
    return{
        "event": EVENT_USER_DELETED,
        "user_id": user_id,
        "email": email,
        "name": name,
        "timestamp": datetime.utcnow().isoformat()
    }
