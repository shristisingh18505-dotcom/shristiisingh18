from flask import Flask
from extensions import db
from models import Student, Teacher, Course, Enrollment
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

def seed(app):
    with app.app_context():
        if not Student.query.first():
            db.session.add_all([
                Student(name="Aarav Mehta", roll_no="S1001", std="10-A", dob="2010-01-15"),
                Student(name="Diya Sharma", roll_no="S1002", std="10-A", dob="2010-06-22"),
            ])
        if not Teacher.query.first():
            db.session.add_all([
                Teacher(name="Ms. Rao", subject="Mathematics"),
                Teacher(name="Mr. Iyer", subject="Science"),
            ])
        if not Course.query.first():
            db.session.add_all([
                Course(name="Algebra & Geometry", code="MATH10"),
                Course(name="Physics Basics", code="SCI10"),
            ])
        db.session.commit()

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    app = create_app()
    if cmd == "init-db":
        seed(app)
        print("Database created and demo data seeded.")
    else:
        print("Usage: python manage.py init-db")
