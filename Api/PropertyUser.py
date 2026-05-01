"""
MyAds Router — مدیریت آگهی‌های کاربر (نیاز به احراز هویت)
POST   /my-ads/            — ایجاد آگهی جدید
GET    /my-ads/            — لیست آگهی‌های خودم
GET    /my-ads/{id}        — جزئیات آگهی خودم
PUT    /my-ads/{id}        — ویرایش آگهی
DELETE /my-ads/{id}        — حذف آگهی
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from Db.Dbase import get_db
from Db.SC import User, Adver
from Auth.JWTAuth import get_current_user
from Schemas.AdverSchema import AdverCreate, AdverUpdate, AdverResponse

router = APIRouter(prefix="/my-ads", tags=["My Advertisements"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_own_adver(adver_id: int, user_id: int, db: Session) -> Adver:
    """Helper: دریافت آگهی و بررسی مالکیت"""
    adver = db.query(Adver).filter(Adver.id == adver_id, Adver.user_id == user_id).first()
    if not adver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="آگهی پیدا نشد یا دسترسی مجاز نیست",
        )
    return adver


@router.post("/", response_model=AdverResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(adver: AdverCreate, db: DBSession, current_user: CurrentUser):
    """ایجاد آگهی جدید"""
    new_adver = Adver(
        **adver.model_dump(),
        user_id=current_user.id,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.add(new_adver)
    db.commit()
    db.refresh(new_adver)
    return new_adver


@router.get("/", response_model=list[AdverResponse])
def get_my_advertisements(db: DBSession, current_user: CurrentUser):
    """لیست آگهی‌های خودم"""
    return db.query(Adver).filter(Adver.user_id == current_user.id).all()


@router.get("/{adver_id}", response_model=AdverResponse)
def get_my_advertisement(adver_id: int, db: DBSession, current_user: CurrentUser):
    """جزئیات یک آگهی خودم"""
    return _get_own_adver(adver_id, current_user.id, db)


@router.put("/{adver_id}", response_model=AdverResponse)
def update_advertisement(
    adver_id: int,
    adver_update: AdverUpdate,
    db: DBSession,
    current_user: CurrentUser,
):
    """ویرایش آگهی"""
    adver = _get_own_adver(adver_id, current_user.id, db)

    update_data = adver_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(adver, field, value)

    db.commit()
    db.refresh(adver)
    return adver


@router.delete("/{adver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(adver_id: int, db: DBSession, current_user: CurrentUser):
    """حذف آگهی"""
    adver = _get_own_adver(adver_id, current_user.id, db)
    db.delete(adver)
    db.commit()
