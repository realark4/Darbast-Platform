from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from Core.Configs import settings
from Db.Dbase import engine
from Db.SC import Base
from Auth.AuthRouter import router as auth_router
from Api.Advertisement import router as advertisement_router
from Api.PropertyUser import router as my_ads_router
from Api.UserDtailes import router as users_router
from Api.Bookmarks import router as bookmarks_router
from Api.Admin import router as admin_router
from AdminUI import init_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ایجاد جداول دیتابیس هنگام startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="DARBast | An AI-powered real estate platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Add session middleware for admin authentication
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY, 
    max_age=settings.ADMIN_SESSION_MAX_AGE,
    https_only=False  # در محیط واقعی روی سرور حتماً True باشد
)
init_admin(app)

# ── Security Headers Middleware ───────────────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production محدود کنید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files ──────────────────────────────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(my_ads_router)
app.include_router(bookmarks_router)
app.include_router(advertisement_router)
app.include_router(admin_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": "2.0.0"}
