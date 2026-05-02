from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from Db.Dbase import get_db
from Db.SC import User
from Core.Configs import settings

# ── Crypto Setup ──────────────────────────────────────────────────────────────

# ── Custom OAuth2 Scheme ─────────────────────────────────────────────────────

class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # First, try to get the token from the Authorization header (standard)
        authorization: str = request.headers.get("Authorization")
        if authorization:
            parts = authorization.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                return parts[1]

        # If not in header, try to get it from the 'access_token' cookie
        return request.cookies.get("access_token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")


# ── Pydantic Models ───────────────────────────────────────────────────────────


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Password Helpers ──────────────────────────────────────────────────────────


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt has a 72-byte limit — truncate to avoid silent mismatch
    pwd_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(pwd_bytes, hashed_password)


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(pwd_bytes)


# ── JWT Helpers ───────────────────────────────────────────────────────────────


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="اعتبارسنجی ناموفق بود",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="حساب کاربری غیرفعال است"
        )
    return user
