"""
Permissions Helper — مدیریت سطوح دسترسی (RBAC)
"""
from fastapi import HTTPException, status, Depends
from typing import Callable

from Db.SC import User
from Auth.JWTAuth import get_current_user


def require_role(allowed_roles: list[str]) -> Callable:
    """Dependency برای بررسی نقش کاربر"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما مجوز دسترسی به این بخش را ندارید"
            )
        return current_user
    return role_checker

# میان‌برهای دسترسی
require_admin = require_role(["admin"])
require_agent = require_role(["admin", "agent"])
require_user = require_role(["admin", "agent", "user"])
