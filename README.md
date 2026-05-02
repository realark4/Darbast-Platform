# 🏢 DARBast - Professional Real Estate Management System

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/JWT-Secure-black?style=for-the-badge&logo=json-web-tokens" alt="JWT" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</div>

*Read this document in other languages: [Persian (فارسی)](README_fa.md)*

---

### 🌐 Introduction
DARBast is a production-ready, feature-rich real estate engine built with FastAPI. It provides a complete solution for property listing, user management, and administrative moderation with a focus on security and high-end UX.

---

## 🛠 Features & Options

### 1. 🔐 Authentication System
| Feature | Description |
| :--- | :--- |
| **Registration** | Secure user sign-up with password hashing (Bcrypt). |
| **Hybrid Login** | Supports both **JWT Bearer Tokens** and **HTTP-only Cookies**. |
| **Persistent Session** | 7-day "Stay Logged In" duration for seamless UX. |
| **Logout** | Complete session termination and cookie clearing. |
| **RBAC** | Role-based access: `Admin`, `Employee`, `Agent`, `User`. |

### 2. 🏠 Property Engine
| Feature | Description |
| :--- | :--- |
| **CRUD Operations** | Create, Read, Update, and Delete ads with owner validation. |
| **Three-State Flow** | Moderation queue: `Pending`, `Approved`, `Rejected`. |
| **Advanced Filtering** | Filter by Location, Price Range, and Transaction Type. |
| **Transaction Types** | Supports `Sell`, `Rent`, `Mortgage`, `Buy`. |
| **Image Gallery** | Multi-image upload support with static file serving. |

### 3. 👤 User Experience
| Feature | Description |
| :--- | :--- |
| **My Ads** | Dedicated dashboard to manage personal advertisements. |
| **Bookmarks** | Save favorite properties for quick access later. |
| **Profile Management** | View and manage personal profile details (`/me`). |

### 4. 🛠 Administrative Power
| Feature | Description |
| :--- | :--- |
| **Security Lockout** | Anti-Brute Force with IP lockout after failed attempts. |
| **Bulk Actions** | Mass approval, suspension, or role promotion. |
| **Custom Dashboard** | Futuristic SVG-based dashboard and OLED design. |
| **Dynamic Formatters** | Visual status badges and image hover previews. |

---

## 🚀 API Endpoints

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

## 🛠 Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy 2.0
- **Security**: Passlib (Bcrypt), Python-Jose (JWT)
- **Admin Interface**: SQLAdmin (Highly Customized)
- **Database**: SQLite (Production-ready schema)
- **Settings**: Pydantic Settings (Environment-based)

---

## 💻 Installation

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
