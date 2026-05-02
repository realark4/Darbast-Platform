from sqladmin import ModelView, expose
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from markupsafe import Markup

from Db.Dbase import engine
from Db.SC import User, Adver, Favourites, AdverImage
from Core.Configs import settings

from Auth.JWTAuth import verify_password


import time
from collections import defaultdict

# ── Anti-Brute Force (In-Memory for simplicity) ─────────────────────────────
_failed_attempts = defaultdict(lambda: {"count": 0, "lockout_until": 0})


class AdminAuth(AuthenticationBackend):
    """سیستم احراز هویت فوق امن برای ورود به رابط کاربری پنل ادمین"""

    async def login(self, request: Request) -> bool:
        client_ip = request.client.host
        current_time = time.time()
        
        # 1. بررسی قفل بودن IP
        attempt_info = _failed_attempts[client_ip]
        if attempt_info["count"] >= settings.ADMIN_MAX_LOGIN_ATTEMPTS:
            if current_time < attempt_info["lockout_until"]:
                return False  # هنوز قفل است
            else:
                # زمان قفل به پایان رسیده، ریست کن
                _failed_attempts[client_ip] = {"count": 0, "lockout_until": 0}

        form = await request.form()
        username, password = form.get("username"), form.get("password")

        # 2. بررسی دیتابیس
        with Session(engine) as db:
            user = db.query(User).filter(User.username == username).first()

            if user and verify_password(password, user.password) and user.role in ["admin", "employee"] and user.is_active:
                # لاگین موفق: ریست کردن تلاش‌های ناموفق
                _failed_attempts[client_ip] = {"count": 0, "lockout_until": 0}
                
                # تنظیم سشن لاگین همراه با زمان ورود برای Time-out
                request.session.update({
                    "token": user.username,
                    "login_time": current_time
                })
                return True

        # لاگین ناموفق: افزایش شمارنده
        attempt_info["count"] += 1
        if attempt_info["count"] >= settings.ADMIN_MAX_LOGIN_ATTEMPTS:
            attempt_info["lockout_until"] = current_time + settings.ADMIN_LOCKOUT_SECONDS
            
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # بررسی وجود توکن
        token = request.session.get("token")
        login_time = request.session.get("login_time", 0)
        
        if not token:
            return False
            
        # 1. بررسی انقضای سشن (Session Timeout)
        if time.time() - login_time > settings.ADMIN_SESSION_MAX_AGE:
            request.session.clear()
            return False
            
        # 2. بررسی مجدد و Real-time نقش کاربر از دیتابیس
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            if not user or user.role not in ["admin", "employee"] or not user.is_active:
                request.session.clear()
                return False
                
        return True


# -----------------------------------------------------
# تعریف ظاهر جداول برای پنل ادمین
# -----------------------------------------------------


from sqladmin import action

class UserAdmin(ModelView, model=User):
    name = "کاربر"
    name_plural = "کاربران"
    icon = "fa-solid fa-users"
    category = "مدیریت دسترسی‌ها"
    
    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role == "admin"

    
    page_size = 20
    page_size_options = [20, 50, 100]
    
    column_list = [
        User.id,
        User.username,
        User.full_name,
        User.email,
        User.role,
        User.is_active,
        User.created_at,
    ]
    
    column_details_list = [
        User.id, User.username, User.full_name, User.email,
        User.role, User.is_active, User.created_at,
        User.advertisements, User.favourites
    ]

    # مشخص کردن فیلدهای قابل ویرایش/ایجاد
    form_columns = [
        User.username,
        User.full_name,
        User.email,
        User.role,
        User.is_active
    ]

    # شخصی سازی باکس های فرم
    form_widget_args = {
        "username": {"placeholder": "مثال: ali_reza"},
        "full_name": {"placeholder": "نام و نام خانوادگی کامل"},
        "email": {"placeholder": "user@example.com"}
    }

    column_labels = {
        User.id: "شناسه",
        User.username: "نام کاربری",
        User.full_name: "نام کامل",
        User.email: "ایمیل",
        User.role: "نقش کاربر",
        User.is_active: "وضعیت اکانت",
        User.created_at: "تاریخ عضویت",
        User.advertisements: "آگهی‌های کاربر",
        User.favourites: "علاقه‌مندی‌ها"
    }

    column_searchable_list = [User.username, User.email, User.full_name]
    column_sortable_list = [User.id, User.created_at, User.role]
    column_default_sort = [(User.id, True)]
    
    export_types = ["csv", "json"]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True

    def format_role(m: User, a):
        colors = {"admin": "danger", "employee": "info", "agent": "warning", "user": "primary"}
        bg = colors.get(m.role, "secondary")
        return Markup(f'<span class="badge bg-{bg}">{m.role.upper()}</span>')
        
    def format_active(m: User, a):
        if m.is_active:
            return Markup('<span class="badge bg-success"><i class="fa fa-check"></i> فعال</span>')
        return Markup('<span class="badge bg-danger"><i class="fa fa-times"></i> مسدود</span>')

    column_formatters = {
        User.role: format_role,
        User.is_active: format_active
    }

    # -- عملیات دسته‌جمعی --
    @action(
        name="suspend_users",
        label="غیرفعال‌سازی دسته‌جمعی ⛔",
        confirmation_message="آیا از مسدودسازی این کاربران اطمینان دارید؟",
        add_in_detail=True,
        add_in_list=True,
    )
    async def suspend_users(self, request: Request, pks: list[any]):
        with Session(engine) as db:
            for pk in pks:
                user = db.query(User).filter(User.id == int(pk)).first()
                if user and user.role not in ["admin", "employee"]: # ادمین ها و کارمندان مسدود نشوند
                    user.is_active = False
            db.commit()
        return "کاربران انتخاب شده مسدود شدند."

    @action(
        name="reactivate_users",
        label="فعال‌سازی مجدد ✅",
        confirmation_message="آیا از فعال‌سازی این کاربران اطمینان دارید؟",
        add_in_detail=True,
        add_in_list=True,
    )
    async def reactivate_users(self, request: Request, pks: list[any]):
        with Session(engine) as db:
            for pk in pks:
                user = db.query(User).filter(User.id == int(pk)).first()
                if user:
                    user.is_active = True
            db.commit()
        return "کاربران انتخاب شده فعال شدند."

    @action(
        name="promote_to_agent",
        label="ارتقا به مشاور 🌟",
        confirmation_message="آیا از ارتقای این کاربران به نقش مشاور اطمینان دارید؟",
        add_in_detail=True,
        add_in_list=True,
    )
    async def promote_to_agent(self, request: Request, pks: list[any]):
        with Session(engine) as db:
            for pk in pks:
                user = db.query(User).filter(User.id == int(pk)).first()
                if user and user.role == "user":
                    user.role = "agent"
            db.commit()
        return "کاربران انتخاب شده به مشاور ارتقا یافتند."


class AdverAdmin(ModelView, model=Adver):
    name = "آگهی"
    name_plural = "آگهی‌ها"
    icon = "fa-solid fa-house-chimney"
    category = "سیستم املاک"
    identity = "adver"


    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role in ["admin", "employee"]


    page_size = 20
    
    column_list = [
        Adver.id,
        Adver.title,
        Adver.price,
        Adver.transaction_type,
        Adver.location,
        Adver.owner,
        Adver.is_active,
        "عملیات"
    ]
    
    def format_actions(m: Adver, a):
        # لینک به صفحه تاییدیه اختصاصی (استفاده از آدرس کلاس اصلی)
        url = f"/admin/adver/approve/{m.id}"
        return Markup(f'<a href="{url}" class="btn btn-sm btn-primary">بررسی آگهی <i class="fa fa-eye"></i></a>')

    @expose("/approve/{id}", methods=["GET", "POST"])
    async def approve_page(self, request: Request):
        from sqlalchemy.orm import joinedload
        from starlette.exceptions import HTTPException
        
        id = request.path_params.get("id")
        with Session(engine) as db:
            model = (
                db.query(Adver)
                .options(joinedload(Adver.owner), joinedload(Adver.images))
                .filter(Adver.id == int(id))
                .first()
            )
            if not model:
                raise HTTPException(status_code=404)

            if request.method == "POST":
                form = await request.form()
                action = form.get("action")
                reason = form.get("rejection_reason", "")

                if action == "approve":
                    model.is_active = True
                    model.rejection_reason = None
                elif action == "reject":
                    model.is_active = False
                    model.rejection_reason = reason or None
                
                db.commit()
                # بازگشت به صفحه‌ای که از آن آمده‌ایم
                referer = request.headers.get("referer")
                return RedirectResponse(
                    url=referer or request.url_for("admin:list", identity="adver"),
                    status_code=302
                )

            # ساخت داده‌های قابل استفاده خارج از session
            context_model = {
                "id": model.id,
                "title": model.title,
                "description": model.description,
                "price": model.price,
                "location": model.location,
                "transaction_type": model.transaction_type,
                "is_active": model.is_active,
                "created_at": model.created_at,
                "rejection_reason": model.rejection_reason,
                "owner_name": model.owner.full_name or model.owner.username if model.owner else "نامشخص",
                "images": [{"image_url": img.image_url, "is_primary": img.is_primary} for img in model.images],
            }

        return await self.templates.TemplateResponse(
            request, 
            "approve_adver.html", 
            {"model": context_model}
        )



    
    column_details_list = [
        Adver.id, Adver.title, Adver.description, Adver.price,
        Adver.transaction_type, Adver.location, Adver.category_id,
        Adver.is_active, Adver.created_at, Adver.owner, Adver.images
    ]

    form_columns = [
        Adver.title,
        Adver.description,
        Adver.price,
        Adver.location,
        Adver.transaction_type,
        Adver.is_active,
        Adver.owner
    ]

    column_labels = {
        Adver.id: "کد آگهی",
        Adver.title: "عنوان",
        Adver.description: "توضیحات",
        Adver.price: "مبلغ (تومان)",
        Adver.transaction_type: "نوع معامله",
        Adver.location: "موقعیت/محله",
        Adver.owner: "صاحب آگهی",
        Adver.is_active: "تاییدیه",
        Adver.created_at: "زمان ثبت",
        Adver.images: "تصاویر",
    }

    column_searchable_list = [Adver.title, Adver.location, Adver.description]
    column_sortable_list = [Adver.price, Adver.created_at]
    column_default_sort = [(Adver.id, True)]


    
    export_types = ["csv", "json", "xls"]
    
    def format_price(m: Adver, a):
        return f"{m.price:,.0f} تومان" if m.price else "-"
        
    def format_active(m: Adver, a):
        if m.is_active:
            return Markup('<span class="badge bg-success">تایید شده</span>')
        if m.rejection_reason:
            return Markup('<span class="badge bg-danger">رد شده</span>')
        return Markup('<span class="badge bg-warning text-dark">در انتظار / معلق</span>')
        
    def format_transaction(m: Adver, a):
        t_types = {"sell": "فروش", "buy": "خرید", "rent": "اجاره", "mortgage": "رهن"}
        val = t_types.get(m.transaction_type, m.transaction_type)
        return Markup(f'<span class="badge bg-info">{val}</span>')

    column_formatters = {
        Adver.price: format_price,
        Adver.is_active: format_active,
        Adver.transaction_type: format_transaction,
        "عملیات": format_actions
    }

    # -- عملیات دسته‌جمعی --
    @action(
        name="approve_adver",
        label="تایید دسته‌جمعی آگهی‌ها ✅",
        confirmation_message="آیا از تایید این آگهی‌ها اطمینان دارید؟",
        add_in_detail=True,
        add_in_list=True,
    )
    async def approve_adver(self, request: Request, pks: list[any]):
        with Session(engine) as db:
            for pk in pks:
                adver = db.query(Adver).filter(Adver.id == int(pk)).first()
                if adver:
                    adver.is_active = True
            db.commit()
        return "آگهی‌ها با موفقیت تایید و منتشر شدند."

    @action(
        name="reject_adver",
        label="رد دسته‌جمعی آگهی‌ها ❌",
        confirmation_message="آیا از رد/معلق کردن این آگهی‌ها اطمینان دارید؟",
        add_in_detail=True,
        add_in_list=True,
    )
    async def reject_adver(self, request: Request, pks: list[any]):
        with Session(engine) as db:
            for pk in pks:
                adver = db.query(Adver).filter(Adver.id == int(pk)).first()
                if adver:
                    adver.is_active = False
            db.commit()
        return "آگهی‌ها معلق شدند."


class PendingAdverAdmin(AdverAdmin):
    name = "تایید آگهی"
    name_plural = "تایید آگهی‌های جدید"
    icon = "fa-solid fa-clock-rotate-left"
    category = "پنل کارمندان"
    identity = "pending_adver"

    
    # محدود کردن کوئری فقط به آگهی‌های غیرفعال و بدون علت رد
    def list_query(self, request: Request):
        return super().list_query(request).filter(Adver.is_active == False, Adver.rejection_reason.is_(None))

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role in ["admin", "employee"]


class ApprovedAdverAdmin(AdverAdmin):
    name = "آگهی تایید شده"
    name_plural = "آگهی‌های تایید شده"
    icon = "fa-solid fa-check-double"
    category = "سیستم املاک"
    identity = "approved_adver"

    def list_query(self, request: Request):
        return super().list_query(request).filter(Adver.is_active == True)


class RejectedAdverAdmin(AdverAdmin):
    name = "آگهی رد شده/حذف شده"
    name_plural = "آگهی‌های رد شده/حذف شده"
    icon = "fa-solid fa-ban"
    category = "پنل کارمندان"
    identity = "rejected_adver"

    def list_query(self, request: Request):
        return super().list_query(request).filter(Adver.is_active == False, Adver.rejection_reason.is_not(None))

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role in ["admin", "employee"]






class FavouritesAdmin(ModelView, model=Favourites):
    name = "علاقه‌مندی"
    name_plural = "علاقه‌مندی‌ها"
    icon = "fa-solid fa-heart"
    category = "تعاملات کاربران"

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role == "admin"


    column_list = [Favourites.id, Favourites.user, Favourites.advertisement]
    form_columns = [Favourites.user, Favourites.advertisement]
    
    column_labels = {
        Favourites.id: "ردیف",
        Favourites.user: "کاربر",
        Favourites.advertisement: "آگهی نشان شده",
    }


class AdverImageAdmin(ModelView, model=AdverImage):
    name = "تصویر آگهی"
    name_plural = "گالری تصاویر"
    icon = "fa-solid fa-images"
    category = "سیستم املاک"

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        with Session(engine) as db:
            user = db.query(User).filter(User.username == token).first()
            return user is not None and user.role in ["admin", "employee"]


    column_list = [
        AdverImage.id,
        AdverImage.image_url,
        AdverImage.adver,
        AdverImage.is_primary,
    ]
    
    form_columns = [
        AdverImage.image_url,
        AdverImage.adver,
        AdverImage.is_primary
    ]

    column_labels = {
        AdverImage.id: "شناسه عکس",
        AdverImage.image_url: "پیش‌نمایش",
        AdverImage.adver: "متعلق به آگهی",
        AdverImage.is_primary: "تصویر اصلی؟",
    }
    
    def format_image(m: AdverImage, a):
        if m.image_url:
            return Markup(f'<img src="{m.image_url}" style="height: 60px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.5)\'" onmouseout="this.style.transform=\'scale(1)\'">')
        return "-"

    column_formatters = {
        AdverImage.image_url: format_image
    }



from sqladmin import Admin
from fastapi import FastAPI

def init_admin(app: FastAPI):
    """Initialize sqladmin with the FastAPI app and register model views."""
    
    # اطمینان از وجود ستون rejection_reason در دیتابیس
    import sqlite3
    try:
        conn = sqlite3.connect("databasex.db")
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE advertisements ADD COLUMN rejection_reason VARCHAR")
        conn.commit()
        conn.close()
    except:
        pass # قبلاً اضافه شده یا خطای دیگر
        
    admin = Admin(

        app, 
        engine, 
        authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
        title="پرتال امن مدیریت دربست",
        base_url="/admin",
        templates_dir="admin_static/templates"
    )

    admin.add_view(UserAdmin)
    admin.add_view(AdverAdmin)
    admin.add_view(ApprovedAdverAdmin)
    admin.add_view(PendingAdverAdmin)
    admin.add_view(RejectedAdverAdmin)
    admin.add_view(AdverImageAdmin)
    admin.add_view(FavouritesAdmin)


    return admin
