from datetime import datetime, date
from extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    std = db.Column(db.String(20))  # class/grade like "10-A"
    dob = db.Column(db.String(20))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
    teacher = db.relationship('Teacher', backref='enrollments')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    att_date = db.Column(db.Date, default=date.today)
    present = db.Column(db.Boolean, default=True)
    enrollment = db.relationship('Enrollment', backref='attendance')

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    assessment = db.Column(db.String(120))  # e.g., "Unit Test 1"
    score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollment = db.relationship('Enrollment', backref='grades')
