# 🏢 DARBast (دربست) - Professional Real Estate Management System

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/JWT-Secure-black?style=for-the-badge&logo=json-web-tokens" alt="JWT" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</div>

---

### 🌐 Introduction / معرفی
**English**: DARBast is a production-ready, feature-rich real estate engine built with FastAPI. It provides a complete solution for property listing, user management, and administrative moderation with a focus on security and high-end UX.

**فارسی**: پروژه «دربست» یک موتور پیشرفته مدیریت املاک و مستغلات است که با FastAPI توسعه یافته است. این سیستم راهکاری جامع برای ثبت آگهی، مدیریت کاربران و نظارت ادمین با تمرکز بر امنیت و تجربه کاربری سطح بالا ارائه می‌دهد.

---

## 🛠 Features & Options (ویژگی‌ها و قابلیت‌ها)

### 1. 🔐 Authentication System (سیستم احراز هویت)
| Feature | Description (English) | توضیحات (فارسی) |
| :--- | :--- | :--- |
| **Registration** | Secure user sign-up with password hashing (Bcrypt). | ثبت‌نام امن کاربر با هش کردن رمز عبور. |
| **Hybrid Login** | Supports both **JWT Bearer Tokens** and **HTTP-only Cookies**. | پشتیبانی همزمان از توکن‌های JWT و کوکی‌های امن. |
| **Persistent Session** | 7-day "Stay Logged In" duration for seamless UX. | قابلیت «مرا به خاطر بسپار» با ماندگاری ۷ روزه. |
| **Logout** | Complete session termination and cookie clearing. | خروج کامل از سیستم و حذف کوکی‌های امنیتی. |
| **RBAC** | Role-based access: `Admin`, `Employee`, `Agent`, `User`. | مدیریت دسترسی بر اساس نقش: ادمین، کارمند، مشاور، کاربر. |

### 2. 🏠 Property Engine (سیستم املاک)
| Feature | Description (English) | توضیحات (فارسی) |
| :--- | :--- | :--- |
| **CRUD Operations** | Create, Read, Update, and Delete ads with owner validation. | مدیریت کامل آگهی‌ها (ایجاد، مشاهده، ویرایش، حذف) با تایید مالکیت. |
| **Three-State Flow** | Moderation queue: `Pending`, `Approved`, `Rejected`. | چرخه نظارت سه مرحله‌ای: معلق، تایید شده، رد شده. |
| **Advanced Filtering** | Filter by Location, Price Range, and Transaction Type. | فیلتر پیشرفته بر اساس محله، محدوده قیمت و نوع معامله. |
| **Transaction Types** | Supports `Sell`, `Rent`, `Mortgage`, `Buy`. | پشتیبانی از انواع معامله: خرید، فروش، رهن و اجاره. |
| **Image Gallery** | Multi-image upload support with static file serving. | پشتیبانی از آپلود چندین تصویر و سرویس‌دهی فایل‌های استاتیک. |

### 3. 👤 User Experience (تجربه کاربری)
| Feature | Description (English) | توضیحات (فارسی) |
| :--- | :--- | :--- |
| **My Ads** | Dedicated dashboard to manage personal advertisements. | داشبورد اختصاصی برای مدیریت آگهی‌های شخصی. |
| **Bookmarks** | Save favorite properties for quick access later. | سیستم نشان کردن (علاقه‌مندی‌ها) برای دسترسی سریع. |
| **Profile Management** | View and manage personal profile details (`/me`). | مشاهده و مدیریت اطلاعات پروفایل کاربری. |

### 4. 🛠 Administrative Power (پنل مدیریت حرفه‌ای)
| Feature | Description (English) | توضیحات (فارسی) |
| :--- | :--- | :--- |
| **Security Lockout** | Anti-Brute Force with IP lockout after failed attempts. | سیستم ضد هک: قفل شدن IP پس از تلاش‌های ناموفق متوالی. |
| **Bulk Actions** | Mass approval, suspension, or role promotion. | عملیات دسته‌جمعی: تایید، مسدودسازی یا ارتقای نقش کاربران. |
| **Custom Dashboard** | Futuristic SVG-based dashboard and OLED design. | داشبورد اختصاصی با المان‌های SVG و طراحی تیره مدرن. |
| **Dynamic Formatters** | Visual status badges and image hover previews. | نمایش بصری وضعیت‌ها با Badge و پیش‌نمایش شناور تصاویر. |

---

## 🚀 API Endpoints (نقاط اتصال)

### Auth & User
- `POST /auth/register` : User registration
- `POST /auth/login` : Secure login (Tokens + Cookies)
- `POST /auth/logout` : Session termination
- `GET /auth/me` : Current profile

### Advertisements
- `GET /advertisement/` : Public list (with filters)
- `GET /advertisement/{id}` : Detailed view
- `POST /my-ads/` : Create new ad
- `POST /my-ads/{id}/images` : Upload property photos
- `GET /bookmarks/` : View saved properties

---

## 🛠 Tech Stack (پشته تکنولوژی)
- **Backend**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy 2.0
- **Security**: Passlib (Bcrypt), Python-Jose (JWT)
- **Admin Interface**: SQLAdmin (Highly Customized)
- **Database**: SQLite (Production-ready schema)
- **Settings**: Pydantic Settings (Environment-based)

---

## 💻 Installation (نصب و راه‌اندازی)

1. **Setup Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .\.venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configuration**:
   Create a `.env` file:
   ```env
   SECRET_KEY="your_secret"
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ADMIN_MAX_LOGIN_ATTEMPTS=5
   ```

3. **Run Application**:
   ```bash
   uvicorn Core.Core:app --reload
   ```

---
<div align="center">
  Developed for High-End Real Estate Portals 🏘️
</div>
