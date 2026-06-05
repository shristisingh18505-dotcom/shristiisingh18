# EduTrack (No-Auth) — School Management System (Flask + SQLite)

Runs without login to avoid auth issues. Manage students, teachers, courses, enrollments, attendance, grades, and **report card PDFs**.

## Quick Start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt

# Create DB and seed demo data
python manage.py init-db

# Run
python app.py
# Open http://127.0.0.1:5000
```
