from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request # Added Request
from fastapi.security import OAuth2PasswordRequestForm # Keep this for OpenAPI docs
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from Db.Dbase import get_db
from Db.SC import User
from Schemas.UserSchema import UserResponse
from Auth.JWTAuth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    Token,
)
from Core.Configs import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr


# ── Register ──────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """ثبت‌نام کاربر جدید"""

    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="این نام کاربری قبلاً ثبت شده است",
        )

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="این ایمیل قبلاً ثبت شده است",
        )

    new_user = User(
        username=request.username,
        password=get_password_hash(request.password),
        email=request.email,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=Token)
async def login(
    response: Response, # Moved to the beginning to fix SyntaxError
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    """ورود کاربر و دریافت توکن JWT"""

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    
    # Set the access token as an HTTP-only cookie
    # secure=True should be used in production with HTTPS
    # samesite="Lax" is a good default for CSRF protection
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=settings.PROJECT_NAME != "Bongah Real Estate API", # Heuristic: True if not default project name (e.g., production)
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, # max_age is in seconds
        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ── Logout ────────────────────────────────────────────────────────────────────

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    """خروج کاربر و حذف کوکی احراز هویت"""
    response.delete_cookie(key="access_token", httponly=True, samesite="Lax", secure=settings.PROJECT_NAME != "Bongah Real Estate API")
    return


# ── Me ────────────────────────────────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """دریافت اطلاعات کاربر لاگین‌شده"""
    return current_user
