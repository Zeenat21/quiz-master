
# Quiz Master V2

**Quiz Master V2** is a full-stack web application designed to help students test their knowledge through quizzes, while allowing administrators to manage subjects, chapters, quizzes, and questions efficiently. It includes scheduled reminders, analytics, and secure role-based access control.

---

## 📌 Project Overview

- A two-role system: **Admin** and **User** 
- Users can register, take quizzes, view scores, receive email reminders and export scores result
- Admins can manage content (CRUD operations on Subject, Chapter, Quiz, Question) and view summary analytics
- Scheduled reminders sent using **Celery** and **Redis** and **Redbeat Scheduler**
- Caching implemented for performance optimization with redis
- Built with **Flask** backend and **Vue.js(Vue CLI)** frontend

---

## ⚙️ Technologies Used

### Backend (Python Flask)
- **Flask** – Web framework
- **Flask-JWT-Extended** – JWT-based authentication
- **Flask-SQLAlchemy** – ORM
- **Flask-Migrate** – DB migrations
- **Flask-Mail** – Email handling
- **Flask-Caching** – Caching with Redis
- **Celery** – Background tasks
- **Redis for windows** –  (Source: [Redis for Windows](https://github.com/tporadowski/redis/releases))
- **RedBeat scheduler** – Scheduling system
- **SQLite** – Database (dev)


### Frontend (Vue CLI 3)
- **Vue.js** – Reactive frontend framework
- **Vue Router** – Routing
- **BootstrapVue** – UI components
- **Axios** – API communication

---

## 📁 Project Structure

```
quiz_master_app/
│
├── backend/                                # Flask backend
│   ├── .vscode/                            # VS Code settings (optional)
│   ├── instance/                           # Flask instance folder (can include db config)
│   ├── migrations/                         # Database migration folder (Flask-Migrate)
│   ├── __pycache__/                        # Python cache (auto-generated)
│   │
│   ├── app.py                              # Entry point of Flask app
│   ├── auth.py                             # Login/Register routes and logic
│   ├── celery_config.py                    # Celery + Redis setup
│   ├── celery_worker.py                    # Starts Celery worker
│   ├── celerybeat-schedule.db              # Celery Beat schedule metadata
│   ├── clear_redbeat.py                    # Script to reset RedBeat schedule store
│   ├── config.py                           # Flask config (JWT, DB, Mail, etc.)
│   ├── dump.rdb                            # Redis database dump
│   ├── extensions.py                       # Initialize extensions like db, jwt (if used)
│   ├── initial_data.py                     # Script to populate default admin/user
│   ├── models.py                           # SQLAlchemy ORM models
│   ├── quiz_master.db                      # SQLite database file (dev only)
│   ├── requirements.txt                    # Python dependencies
│   ├── routes.py                           # Main API endpoints
│   ├── tasks_celery.py                     # Background tasks for reminders, etc.
│   └── test.py                             # Test script or sandbox file
│
├── frontend/                               # Vue frontend
│   ├── node_modules/                       # Node dependencies
│   ├── public/                             # Static public files
│   │   ├── favicon.ico
│   │   └── index.html                      # HTML root template
│   │
│   ├── src/                                # Source folder
│   │   ├── assets/                         # Images, fonts, static assets
│   │   ├── components/                     # Reusable Vue components (e.g., Sidebar, Cards)
│   │   ├── plugins/                        # BootstrapVue, FontAwesome, etc.
│   │   ├── router/                         # Vue Router setup (index.js, routes config)
│   │   ├── store/                          # Vuex store for global state
│   │   ├── views/                          # Main page views
│   │   │   ├── Admin/                      # Admin dashboard views
│   │   │   ├── User/                       # User dashboard views
│   │   │   ├── About.vue
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── App.vue                         # Root Vue component
│   │   ├── axios.js                        # Axios config + interceptors for JWT
│   │   └── main.js                         # App bootstrap
│   │
│   ├── jsconfig.json                       # JS/IDE project config
│   ├── package-lock.json                   # Locked versions of npm packages
│   └── package.json                        # Project metadata + scripts
│
├── README.md                               # Project overview and setup instructions
└── .gitignore                              # Files to ignore in version control

---

## 🔐 Key Features

### ✅ Authentication & Roles
- JWT-based secure login
- Separate roles: Admin and User

### 📊 Admin Features
- Add/edit/delete: Subjects, Chapters, Quizzes, Questions
- View user quiz performance and summary charts
- Search users, subjects, and quizzes
- Caching enabled on dashboards

### 🧑‍🎓 User Features
- Register, log in, and view profile
- Browse quizzes by subject/chapter
- Attempt quizzes and view scores
- Configure daily email reminders

### 📬 Reminders & Background Tasks
- Users can choose daily reminder time
- Celery + Redis handles scheduling
- `ScheduledTaskLog` tracks task executions
- `Reminder` model stores preferences

---

## 🚀 How to Run

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run serve
```

### Celery Worker
```bash
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

### Celery Beat Scheduler
```bash
celery -A celery_worker beat --scheduler redbeat.RedBeatScheduler --loglevel=info
```

> Ensure Redis is running locally: `redis-server`

---

## 📜 API Design

- APIs grouped using Flask Blueprints:
  - `/api/register`, `/api/login` → Auth routes
  - `/admin/...` → Admin routes
  - `/user/...` → User-specific routes
- Routes return JSON responses; secured with JWT

---

## 🧠 LLM/AI Usage

- ~30–35% of the project leveraged AI tools (ChatGPT) for:
  - Writing boilerplate code
  - Optimizing route design and Celery setup
  - Generating UI enhancements

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

Special thanks to the course instructors at IITM, my techie friend Ateeq and my fellow IITM students.
