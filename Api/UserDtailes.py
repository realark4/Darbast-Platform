"""
UserDetails Router — مدیریت پروفایل کاربر (نیاز به احراز هویت)
GET  /users/me            — مشاهده پروفایل
PUT  /users/me            — ویرایش پروفایل
GET  /users/me/stats      — آمار آگهی‌های کاربر
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from Db.Dbase import get_db
from Db.SC import User, Adver
from Auth.JWTAuth import get_current_user
from Schemas.UserSchema import UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: CurrentUser):
    """مشاهده پروفایل کاربر جاری"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_profile(user_data: UserUpdate, db: DBSession, current_user: CurrentUser):
    """ویرایش پروفایل"""
    if user_data.email:
        conflict = db.query(User).filter(
            User.email == user_data.email,
            User.id != current_user.id,
        ).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="این ایمیل قبلاً توسط کاربر دیگری استفاده شده است",
            )
        current_user.email = user_data.email

    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/stats")
def get_my_stats(db: DBSession, current_user: CurrentUser):
    """آمار آگهی‌های کاربر جاری"""
    total = db.query(Adver).filter(Adver.user_id == current_user.id).count()
    active = db.query(Adver).filter(Adver.user_id == current_user.id, Adver.is_active == True).count()
    return {
        "username": current_user.username,
        "total_advertisements": total,
        "active_advertisements": active,
        "member_since": current_user.created_at or "N/A",
    }