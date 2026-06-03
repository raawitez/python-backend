from app.messaging.rabbitmq_client import publisher
from app.messaging.events import (
    QUEUE_USER_EVENTS,
    build_user_updated_event,
    build_user_deleted_event
)


def update_user(
    self, user_id: int, name: str, email: str,
    age: int, password: str, bio=None
):
    user = self._get_user_or_404(user_id)

    # Track what changed for the event
    changes = {}
    if user.name  != name:  changes["name"]  = name
    if user.email != email: changes["email"] = email
    if user.age   != age:   changes["age"]   = age
    if user.bio   != bio:   changes["bio"]   = bio

    user.name     = name
    user.email    = email
    user.age      = age
    user.password = password
    user.bio      = bio

    self.db.commit()
    self.db.refresh(user)

    # Invalidate cache
    delete_cache(CACHE_ALL_USERS)
    delete_cache(f"user:{user_id}")

    # Publish event if something actually changed
    if changes:
        event = build_user_updated_event(
            user_id=user_id,
            changes=changes
        )
        publisher.publish(QUEUE_USER_EVENTS, event)

    return user


def delete_user(self, user_id: int):
    user  = self._get_user_or_404(user_id)
    email = user.email
    name  = user.name

    self.db.delete(user)
    self.db.commit()

    # Invalidate cache
    delete_cache(CACHE_ALL_USERS)
    delete_cache(f"user:{user_id}")

    # Publish event
    event = build_user_deleted_event(
        user_id=user_id,
        email=email,
        name=name
    )
    publisher.publish(QUEUE_USER_EVENTS, event)

    return {
        "message": f"User {user_id} deleted successfully",
        "email":   email,
        "name":    name
    }