from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AdverBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="عنوان آگهی")
    description: str = Field(..., min_length=10, description="توضیحات آگهی")
    price: float = Field(..., ge=0, description="قیمت (تومان)")
    location: str = Field(..., min_length=2, description="موقعیت مکانی")


class AdverCreate(AdverBase):
    category_id: Optional[int] = Field(None, description="شناسه دسته‌بندی")


class AdverUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    price: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, min_length=2)
    is_active: Optional[bool] = None


class AdverResponse(AdverBase):
    id: int
    user_id: int
    category_id: Optional[int] = None
    is_active: bool
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}
