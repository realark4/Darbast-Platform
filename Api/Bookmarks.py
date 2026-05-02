"""
Bookmarks Router — مدیریت علاقه‌مندی‌های کاربر
POST   /bookmarks/{adver_id}  — افزودن به علاقه‌مندی‌ها
DELETE /bookmarks/{adver_id}  — حذف از علاقه‌مندی‌ها
GET    /bookmarks/            — لیست آگهی‌های نشان‌شده
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from Db.Dbase import get_db
from Db.SC import User, Adver, Favourites
from Auth.JWTAuth import get_current_user
from Schemas.AdverSchema import AdverResponse

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/{adver_id}", status_code=status.HTTP_201_CREATED)
def add_bookmark(adver_id: int, db: DBSession, current_user: CurrentUser):
    """افزودن یک آگهی به علاقه‌مندی‌ها (نشان‌شده‌ها)"""
    
    # 1. بررسی وجود آگهی
    adver = db.query(Adver).filter(Adver.id == adver_id, Adver.is_active == True).first()
    if not adver:
        raise HTTPException(status_code=404, detail="آگهی پیدا نشد")

    # 2. بررسی اینکه قبلا اضافه نشده باشد
    existing = db.query(Favourites).filter(
        Favourites.user_id == current_user.id,
        Favourites.advertisement_id == adver_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="این آگهی قبلاً در نشان‌شده‌های شما قرار گرفته است")

    # 3. افزودن به دیتابیس
    new_bookmark = Favourites(user_id=current_user.id, advertisement_id=adver_id)
    db.add(new_bookmark)
    db.commit()
    
    return {"message": "با موفقیت به علاقه‌مندی‌ها اضافه شد"}


@router.delete("/{adver_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bookmark(adver_id: int, db: DBSession, current_user: CurrentUser):
    """حذف یک آگهی از علاقه‌مندی‌ها"""
    bookmark = db.query(Favourites).filter(
        Favourites.user_id == current_user.id,
        Favourites.advertisement_id == adver_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="در علاقه‌مندی‌های شما پیدا نشد")

    db.delete(bookmark)
    db.commit()
    return


@router.get("/", response_model=list[AdverResponse])
def get_my_bookmarks(db: DBSession, current_user: CurrentUser):
    """لیست آگهی‌های علاقه‌مندی من"""
    bookmarks = db.query(Favourites).filter(Favourites.user_id == current_user.id).all()
    # Extract the advertisement objects from the bookmarks
    bookmarked_ads = [b.advertisement for b in bookmarks if b.advertisement.is_active]
    return bookmarked_ads
