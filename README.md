# 📘 CAMPULSE — Backend (MVP)

> A simple, student-first productivity companion for Nigerian university students.

## 🎯 Aim & Vision

**Core Problem:** Nigerian students struggle with missing deadlines, scattered information, unreliable updates, and a lack of legitimate opportunities (gigs, scholarships).

**Solution:** Campulse is a smart, central hub that fits how students live — fast, simple, and mobile-first. It combines an academic planner with a curated opportunities hub and tutor discovery.

**MVP Goal:** Build the simplest usable version with 3 core modules:
1.  **Smart Academic Planner**: Manage classes, assignments, and exams.
2.  **Campus Opportunities Hub**: Find legit gigs, scholarships, and deals.
3.  **Tutor Discovery**: Connect with tutors for academic support.

## 🏗️ Architecture

The backend is built with a modern, high-performance Python stack designed for speed and simplicity.

*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to learn, fast to code, ready for production.
*   **Database ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - Combines SQLAlchemy and Pydantic for intuitive database interaction.
*   **Database**: **SQLite** (for MVP) - Zero-config, serverless, file-based database. Easily scalable to PostgreSQL.
*   **Authentication**: **JWT (JSON Web Tokens)** - Secure, stateless authentication.
*   **Password Hashing**: **Bcrypt** - Industry-standard password security.

### Project Structure

```
campulse_backend/
├── app/
│   ├── main.py          # Application entry point
│   ├── core/            # Configuration & Security (JWT, Hashing)
│   ├── models/          # Database Models (User, Task, Opportunity, Tutor)
│   ├── api/             # API Route Handlers
│   │   ├── v1/endpoints # Individual module endpoints
│   │   └── deps.py      # Dependency Injection (Current User)
│   └── db/              # Database Session Management
├── seed.py              # Database Seeding Script
└── verify_api.py        # API Verification Script
```

## 🔌 API Documentation

The API is organized into versioned endpoints (`/api/v1`).

### 🔐 Authentication
*   `POST /api/v1/auth/signup`: Register a new user (School, Department, Level).
*   `POST /api/v1/auth/login`: Authenticate and receive a JWT access token.
*   `GET /api/v1/auth/me`: Get current user profile.

### 📅 Academic Planner (`/tasks`)
*   `GET /`: List all tasks (assignments, tests, classes).
*   `POST /`: Create a new task with priority and due date.
*   `PATCH /{id}`: Update a task (mark as done, edit details).
*   `DELETE /{id}`: Remove a task.

### 🚀 Opportunities Hub (`/opportunities`)
*   `GET /`: Browse opportunities (Gigs, Scholarships, Deals). Filter by category.
*   `GET /{id}`: View details of a specific opportunity.
*   `POST /{id}/bookmark`: Save an opportunity for later.

### 🎓 Tutor Discovery (`/tutors`)
*   `GET /`: Find tutors. Filter by course code (e.g., "MTH 101").
*   `GET /{id}`: View tutor details and WhatsApp contact.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   `pip`

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repo-url>
    cd campulse_backend
    ```

2.  **Install Dependencies**
    ```bash
    pip install -e .
    ```

3.  **Run the Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

4.  **Explore the Docs**
    Open your browser to `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### Seeding Data
To populate the database with initial opportunities and tutors:
```bash
python seed.py
```
