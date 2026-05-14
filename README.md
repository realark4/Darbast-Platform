# 🏢 DARBast - Professional Real Estate Management System

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/JWT-Secure-black?style=for-the-badge&logo=json-web-tokens" alt="JWT" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</div>

<p align="center">
  <em>A production-ready, highly secure, and feature-rich real estate platform backend.</em>
</p>

*Read this document in other languages: [Persian (فارسی)](README_fa.md)*

---

## 🌐 Introduction
**DARBast** is a comprehensive, production-ready real estate engine built purely with **FastAPI** and **SQLAlchemy**. It provides a robust and scalable architecture for property listing, user management, and administrative moderation. Focusing on security and high-end UX, DARBast supports modern authentication flows, role-based access control (RBAC), and a dynamic state machine for advertisement approvals.

---

## 🛠 Features & Capabilities

### 1. 🔐 Advanced Authentication System
- **Secure Registration:** Passwords are hashed using state-of-the-art `Bcrypt`.
- **Hybrid Login System:** Supports dual authentication via **JWT Bearer Tokens** and **HTTP-only Cookies** for maximum flexibility and security.
- **Persistent Sessions:** "Remember Me" functionality offering a seamless 7-day session duration.
- **Role-Based Access Control (RBAC):** Hierarchical permission levels (`Admin`, `Employee`, `Agent`, `User`).
- **Anti-Brute Force:** IP lockout mechanisms after sequential failed login attempts.

### 2. 🏠 Property Management Engine
- **Full CRUD Operations:** Create, Read, Update, and Delete advertisements strictly validated by ownership.
- **Moderation Workflow:** Three-state ad moderation queue (`Pending`, `Approved`, `Rejected`) managed by admins.
- **Advanced Filtering:** Query properties using parameters like Location, Price Range, and Transaction Type (`Sell`, `Rent`, `Mortgage`, `Buy`).
- **Media Gallery:** Robust multi-image upload handling coupled with static file serving.

### 3. 👤 User Experience
- **Personal Dashboard (`My Ads`):** Dedicated space for users to manage their listings.
- **Bookmarks:** Save and retrieve favorite properties effortlessly.
- **Profile Management:** Intuitive endpoints (`/me`) to manage user credentials and information.

### 4. 🛠 Administrative Power (SQLAdmin)
- **Custom Admin Dashboard:** Overhauled UI featuring an OLED aesthetic and SVG visual elements.
- **Bulk Operations:** Execute mass approvals, rejections, or account suspensions.
- **Dynamic Formatting:** Visual badges and interactive hover states for image previews within the admin panel.

---

## 📂 Project Structure

```text
DARBast-Platform/
├── Api/               # REST API Routers and Endpoints
├── Auth/              # Authentication flows, JWT handling, and RBAC
├── Core/              # FastAPI Application Factory & Configurations
├── Db/                # SQLAlchemy Models, Database setup & Session handling
├── Migration/         # Alembic migration scripts
├── Schemas/           # Pydantic models for serialization and validation
├── admin_static/      # Custom SQLAdmin UI templates
├── alembic.ini        # Alembic configuration
└── requirements.txt   # Python dependencies
```

---

## 🚀 API Endpoints Overview

### Authentication (`/auth`)
- `POST /auth/register` : Create a new user account.
- `POST /auth/login` : Authenticate and receive JWT + Secure Cookies.
- `POST /auth/logout` : Terminate session securely.
- `GET /auth/me` : Retrieve current user profile.

### Advertisements (`/advertisement` & `/my-ads`)
- `GET /advertisement/` : Fetch all approved public properties (supports filtering).
- `GET /advertisement/{id}` : Detailed view of a specific property.
- `POST /my-ads/` : Create a new property listing.
- `POST /my-ads/{id}/images` : Upload images to a specific property.
- `GET /bookmarks/` : Retrieve user's saved properties.

---

## 💻 Installation & Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/your-username/DARBast-Platform.git
cd DARBast-Platform
```

### 2. Setup Virtual Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On Linux/MacOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory based on your environment:
```env
SECRET_KEY="your_super_secret_key_here"
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ADMIN_MAX_LOGIN_ATTEMPTS=5
```

### 5. Database Migrations
Initialize your database with the latest Alembic migrations:
```bash
alembic upgrade head
```

### 6. Run the Application
Start the FastAPI server:
```bash
uvicorn Core.Core:app --reload
```
The API documentation will be accessible at: `http://localhost:8000/docs`

---
<div align="center">
  <p><i>Developed for High-End Real Estate Portals 🏘️</i></p>
</div>
