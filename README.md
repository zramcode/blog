# blog
A full-featured blog application built with FastAPI, supporting user authentication, post management, file uploads, caching, background tasks, and more.

⚙️ Tech Stack
Python 3.10+

FastAPI – Modern web framework

SQLAlchemy – ORM for database access

OAuth2 with JWT – User authentication

bcrypt – Password hashing

FastAPI Pagination – Paginate large results

File Uploads – User avatars or post images

Redis + fastapi-cache – Caching system

Celery + Redis – Background email sending

Pydantic – Data validation

Uvicorn – ASGI server

✅ Features
User registration and login

Secure password hashing with bcrypt

JWT access token authentication

Protected routes with role-based access

CRUD operations for blog posts

Image upload for user profile

Full-text search on posts (title, author, slug)

Pagination for post listing

Background email sending via Celery

Caching of expensive endpoints using Redis

Interactive API documentation with Swagger UI

📦 Project Structure (example)
bash
Copy
Edit
.
├── app/
│   ├── main.py
│   ├── routers/
│   ├── db/
│   ├── models/
│   ├── operations/
│   └── auth/
│   └── configs/
├── static/                # Uploaded image files
├── celery_worker.py             # Celery worker file
├── requirements.txt
├── README.md

🚀 Getting Started
bash
Copy
Edit
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
uvicorn main:app --reload
🧰 Background Tasks
Start Redis and Celery (optional for background email tasks):

bash
Copy
Edit
# Start Redis (if installed locally)
redis-server

# Start Celery worker
celery -A worker.celery worker --loglevel=info
📮 Main API Endpoints
Method	Endpoint	Description
POST	/register	User registration
POST	/login	Get JWT access token
GET	/posts	List all blog posts
GET	/posts/search	Search posts
GET	/users/me	Get current user info
POST	/upload	Upload profile image
