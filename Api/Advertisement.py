"""
Advertisement Router — مسیرهای عمومی آگهی‌ها
GET /advertisement/          — لیست همه آگهی‌های فعال
GET /advertisement/{id}      — جزئیات یک آگهی
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from Db.Dbase import get_db
from Db.SC import Adver
from Schemas.AdverSchema import AdverResponse, TransactionType

router = APIRouter(prefix="/advertisement", tags=["Advertisement"])

DBSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[AdverResponse])
def list_advertisements(
    db: DBSession,
    skip: int = Query(0, ge=0, description="تعداد رکورد برای رد شدن"),
    limit: int = Query(20, ge=1, le=100, description="حداکثر تعداد نتایج"),
    location: Optional[str] = Query(None, description="فیلتر بر اساس موقعیت"),
    min_price: Optional[float] = Query(None, ge=0, description="حداقل قیمت"),
    max_price: Optional[float] = Query(None, ge=0, description="حداکثر قیمت"),
    transaction_type: Optional[TransactionType] = Query(None, description="نوع معامله (خرید، فروش، رهن، اجاره)"),
):
    """لیست همه آگهی‌های فعال با قابلیت فیلتر"""
    query = db.query(Adver).filter(Adver.is_active == True)

    if location:
        query = query.filter(Adver.location.ilike(f"%{location}%"))
    if min_price is not None:
        query = query.filter(Adver.price >= min_price)
    if max_price is not None:
        query = query.filter(Adver.price <= max_price)
    if transaction_type:
        query = query.filter(Adver.transaction_type == transaction_type)

    return query.offset(skip).limit(limit).all()


@router.get("/{adver_id}", response_model=AdverResponse)
def get_advertisement(adver_id: int, db: DBSession):
    """جزئیات یک آگهی خاص"""
    adver = db.query(Adver).filter(Adver.id == adver_id, Adver.is_active == True).first()
    if not adver:
        raise HTTPException(status_code=404, detail="آگهی پیدا نشد")
    return adver
