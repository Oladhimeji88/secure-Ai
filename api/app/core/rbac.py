from collections.abc import Sequence
from fastapi import Depends, HTTPException, status

from app.models.user import Role, User
from app.routers.auth import get_current_user


def require_roles(allowed: Sequence[Role]):
    def _guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return _guard
