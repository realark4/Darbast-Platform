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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ایجاد جداول دیتابیس هنگام startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="پلتفرم هوش مصنوعی بنگاه باشی",
    version="2.0.0",
    lifespan=lifespan,
)

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
