"""
Admin Router — پنل مدیریت (فقط برای ادمین‌ها)
PUT    /admin/advertisement/{id}/toggle-status  — تغییر وضعیت تایید/رد آگهی
DELETE /admin/advertisement/{id}                — حذف آگهی توسط ادمین
GET    /admin/users                             — لیست کاربران
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from Db.Dbase import get_db
from Db.SC import User, Adver
from Auth.Permissions import require_admin
from Schemas.AdverSchema import AdverResponse

router = APIRouter(prefix="/admin", tags=["Admin Panel"], dependencies=[Depends(require_admin)])

DBSession = Annotated[Session, Depends(get_db)]


@router.put("/advertisement/{adver_id}/toggle-status")
def toggle_advertisement_status(adver_id: int, db: DBSession):
    """تغییر وضعیت فعال/غیرفعال بودن آگهی (تایید یا مسدودسازی)"""
    adver = db.query(Adver).filter(Adver.id == adver_id).first()
    if not adver:
        raise HTTPException(status_code=404, detail="آگهی پیدا نشد")
        
    adver.is_active = not adver.is_active
    db.commit()
    db.refresh(adver)
    
    status_str = "فعال" if adver.is_active else "غیرفعال"
    return {"message": f"وضعیت آگهی با موفقیت به '{status_str}' تغییر یافت", "is_active": adver.is_active}


@router.delete("/advertisement/{adver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement_by_admin(adver_id: int, db: DBSession):
    """حذف زوری یک آگهی متخلف توسط ادمین"""
    adver = db.query(Adver).filter(Adver.id == adver_id).first()
    if not adver:
        raise HTTPException(status_code=404, detail="آگهی پیدا نشد")
        
    db.delete(adver)
    db.commit()
    return


@router.get("/users")
def get_all_users(db: DBSession):
    """دریافت لیست تمام کاربران توسط ادمین"""
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]
