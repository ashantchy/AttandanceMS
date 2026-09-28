<!-- STREAMING_CHUNK:Documenting project header and overview... -->
# Attendance & Leave Management System (FastAPI)

A lightweight, asynchronous backend application built with **FastAPI**, **Clean Architecture**, and **MySQL**, designed to manage staff registration, login/logout attendance tracking, and leave requests.

---

<!-- STREAMING_CHUNK:Outlining system architecture... -->
## 🏗️ Architecture Overview

The project adheres to Clean Architecture principles, ensuring a clear separation of concerns across layers:

```main_app
lib/attend/
├── domain/            # Core business models & Pydantic schemas
│   ├── models.py      # Domain dataclasses & SQLAlchemy ORM models
│   └── schemas.py     # API request/response validation
├── repository/        # Data access layer (MySQL / aiomysql)
│   ├── database.py    # Async connection pool & cursor setup
│   ├── staff_repository.py
│   └── attendance_repository.py
├── services/          # Business logic layer
│   ├── security.py    # Password hashing & verification via bcrypt
│   ├── staff_service.py
│   └── attendance_service.py
└── routers/           # HTTP presentation layer (Endpoints)
    ├── staff_router.py
    └── attendance_router.py
```

---

<!-- STREAMING_CHUNK:Listing core system features... -->
## 🛠️ Features

- **Staff Registration**: Create new staff accounts with secure `bcrypt` password hashing.
- **Attendance Management**:
  - Email & Password authentication for Login/Logout.
  - Active session prevention (prevents duplicate logins without logging out first).
  - Duration calculation in minutes upon logout.
- **Leave Management**:
  - **Regular Leave**: Submits leave requests with `PENDING` status for manager review.
  - **Emergency Leave**: Automatically sets status to `AUTO_APPROVED`.
  - **Leave Approval**: Endpoint for managers to approve/reject pending leaves.
- **Database Operations**: Asynchronous database interaction powered by `aiomysql` and managed via **Alembic** migrations.

---

<!-- STREAMING_CHUNK:Writing installation and setup guidelines... -->
## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher (Python 3.13 supported)
- **Database**: MySQL Server (e.g., via phpMyAdmin / XAMPP)
- **Virtual Environment**: `venv`

---

### Installation & Setup

1. **Clone the Repository & Navigate to Directory**
   ```bash
   cd fast
   ```

2. **Activate Virtual Environment**
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn aiomysql pymysql sqlalchemy alembic python-dotenv bcrypt pydantic
   ```

4. **Environment Configuration**
   Create a `.local.properties` file in the root directory:
   ```properties
   HOST=localhost
   DB_USER=root
   PASSWORD=
   DATABASE=attendance_db
   PORT=3306
   AUTOCOMMIT=True
   ```
   > ⚠️ **Note**: Ensure `.local.properties` is listed in your `.gitignore` file.

5. **Database Setup & Migrations**
   Make sure your MySQL server is running and the database `attendance_db` exists in phpMyAdmin. Run Alembic migrations to build the schema:
   ```bash
   # Generate migration script
   alembic revision --autogenerate -m "create tables"

   # Apply schema to database
   alembic upgrade head
   ```

---

<!-- STREAMING_CHUNK:Providing server execution commands... -->
## 🏃 Running the Application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

<!-- STREAMING_CHUNK:Detailing API endpoints table... -->
## 📡 API Endpoints Overview

### Staff Management (`/staff`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/staff/` | Register a new staff member |

### Attendance & Leaves (`/attendance`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/attendance/login` | Authenticate using `email` & `password` to record login |
| `POST` | `/attendance/logout` | Authenticate using `email` & `password` to calculate duration & record logout |
| `POST` | `/attendance/leave/regular` | Submit a regular leave request (`PENDING`) |
| `POST` | `/attendance/leave/emergency` | Submit an emergency leave request (`AUTO_APPROVED`) |
| `PUT` | `/attendance/leave/{leave_id}/approve` | Approve or reject a leave request (Manager restricted) |

---

<!-- STREAMING_CHUNK:Providing sample request payloads... -->
## 🧪 Sample Request Payloads

### 1. Register Staff (`POST /staff/`)
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "SecurePassword123",
  "department": "Engineering",
  "role": "staff"
}
```

### 2. Login (`POST /attendance/login`)
```json
{
  "email": "jane.doe@example.com",
  "password": "SecurePassword123"
}
```

### 3. Logout (`POST /attendance/logout`)
```json
{
  "email": "jane.doe@example.com",
  "password": "SecurePassword123"
}
```

### 4. Regular Leave Request (`POST /attendance/leave/regular`)
```json
{
  "staff_id": 1,
  "leave_date": "2026-10-01",
  "reason": "Family obligation"
}
```

---

<!-- STREAMING_CHUNK:Adding security details and best practices... -->
## 🔒 Security Measures

- Passwords are encrypted prior to storage using `bcrypt` salting and hashing.
- Inputs are automatically truncated to 72 bytes before processing to remain within `bcrypt` specifications.
- Application configurations and secrets are isolated from source code using `.local.properties`.