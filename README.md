# 🏢 Bongah (بنگاه) - Real Estate API

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLAlchemy" />
</div>

یک پلتفرم جامع و مدرن برای مدیریت املاک و مستغلات (بنگاه املاک) که با استفاده از **FastAPI** توسعه داده شده است. این سیستم به گونه‌ای طراحی شده تا همزمان مقیاس‌پذیر، امن و سریع باشد.

## 🚀 ویژگی‌های فعلی (Current Features)
* **معماری ماژولار**: استفاده از ساختار استاندارد FastAPI برای توسعه و نگهداری آسان.
* **احراز هویت پیشرفته (JWT & Cookies)**:
  * پشتیبانی از لاگین دائمی (Stay Logged In) به مدت ۷ روز.
  * استفاده از `HTTP-only Cookies` برای بالاترین سطح امنیت وب و جلوگیری از حملات XSS.
  * پشتیبانی همزمان از `Bearer Token` در Header برای کلاینت‌های موبایل و API.
* **امنیت رمز عبور**: هش کردن رمزهای عبور با الگوریتم قدرتمند `Bcrypt`.
* **مدیریت نشست‌ها**: قابلیت لاگین و لاگ‌اوت یکپارچه.
* **دیتابیس**: یکپارچه‌سازی با SQLAlchemy.

## 🛠 تکنولوژی‌های استفاده شده
* **فریم‌ورک**: FastAPI
* **دیتابیس ORM**: SQLAlchemy
* **امنیت و هش**: Passlib & Bcrypt
* **احراز هویت**: python-jose (JWT)
* **مدیریت متغیرهای محیطی**: Pydantic Settings

## 🗺 نقشه راه (Roadmap)
ویژگی‌هایی که در آینده به این پلتفرم اضافه خواهند شد:
- [ ] مدیریت آگهی‌های املاک (ثبت، ویرایش، حذف).
- [ ] جستجوی پیشرفته و فیلترینگ (بر اساس قیمت، متراژ، محله و...).
- [ ] سیستم آپلود تصاویر برای آگهی‌ها.
- [ ] سطوح دسترسی کاربران (ادمین، مشاور املاک، کاربر عادی).
- [ ] ذخیره و علاقه‌مندی‌ها (Bookmarking).
- [ ] سیستم چت یا پیام‌رسانی بین کاربر و مشاور.

## 💻 نحوه اجرا
1. ایجاد محیط مجازی: `python -m venv .venv`
2. فعال‌سازی محیط: `.\.venv\Scripts\activate`
3. نصب نیازمندی‌ها: `pip install -r requirements.txt` (در صورت وجود)
4. اجرای سرور: `uvicorn Core.Core:app --reload`
