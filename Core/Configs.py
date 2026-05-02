from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "DARBast Real Estate API"
    DATABASE_URL: str = "sqlite:///databasex.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days (7 * 24 * 60)

    # ── Security Settings ─────────────────────────────────────────────────────
    # تعداد حداکثر تلاش‌های ناموفق ورود ادمین قبل از قفل شدن
    ADMIN_MAX_LOGIN_ATTEMPTS: int = 5
    # مدت قفل حساب ادمین (ثانیه)
    ADMIN_LOCKOUT_SECONDS: int = 300  # 5 minutes
    # مدت زمان انقضای سشن ادمین (ثانیه)
    ADMIN_SESSION_MAX_AGE: int = 3600  # 1 hour

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
