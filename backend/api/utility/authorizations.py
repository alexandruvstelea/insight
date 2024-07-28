from functools import wraps
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if user.role not in role:
                logger.error("User not authorized to perform this action.")
                raise HTTPException(status_code=403, detail="User not authorized.")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
