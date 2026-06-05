from flask import Flask, render_template, redirect, url_for, request, flash, send_file, jsonify
from config import Config
from extensions import db, csrf
from models import *
from forms import *
from utils.pdf_report import report_card
from flask import Blueprint
from datetime import date

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    csrf.init_app(app)
    return app

app = create_app()
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return redirect(url_for("main.dashboard"))

@main.route("/dashboard")
def dashboard():
    data = {
        "students": Student.query.count(),
        "teachers": Teacher.query.count(),
        "courses": Course.query.count(),
        "enrollments": Enrollment.query.count(),
    }
    return render_template("dashboard.html", data=data)

# Students
@main.route("/students", methods=["GET","POST"])
def students():
    form = StudentForm()
    if form.validate_on_submit():
        s = Student(name=form.name.data, roll_no=form.roll_no.data, std=form.std.data, dob=form.dob.data)
        db.session.add(s); db.session.commit()
        flash("Student saved.", "success"); return redirect(url_for("main.students"))
    items = Student.query.order_by(Student.id).all()
    return render_template("students.html", form=form, items=items)

# Teachers
@main.route("/teachers", methods=["GET","POST"])
def teachers():
    form = TeacherForm()
    if form.validate_on_submit():
        t = Teacher(name=form.name.data, subject=form.subject.data)
        db.session.add(t); db.session.commit()
        flash("Teacher saved.", "success"); return redirect(url_for("main.teachers"))
    items = Teacher.query.order_by(Teacher.id).all()
    return render_template("teachers.html", form=form, items=items)

# Courses
@main.route("/courses", methods=["GET","POST"])
def courses():
    form = CourseForm()
    if form.validate_on_submit():
        c = Course(name=form.name.data, code=form.code.data)
        db.session.add(c); db.session.commit()
        flash("Course saved.", "success"); return redirect(url_for("main.courses"))
    items = Course.query.order_by(Course.id).all()
    return render_template("courses.html", form=form, items=items)

# Enroll
@main.route("/enroll", methods=["GET","POST"])
def enroll():
    form = EnrollForm()
    if form.validate_on_submit():
        e = Enrollment(student_id=form.student_id.data, course_id=form.course_id.data, teacher_id=form.teacher_id.data)
        db.session.add(e); db.session.commit()
        flash("Enrollment saved.", "success"); return redirect(url_for("main.enroll"))
    students = Student.query.order_by(Student.id).all()
    courses = Course.query.order_by(Course.id).all()
    teachers = Teacher.query.order_by(Teacher.id).all()
    return render_template("enroll.html", form=form, students=students, courses=courses, teachers=teachers)

# Attendance
@main.route("/attendance", methods=["GET","POST"])
def attendance():
    form = AttendanceForm()
    enrolled = []
    if request.method == "POST" and form.validate_on_submit():
        c_id = form.course_id.data
        d = form.att_date.data
        # clear duplicates for same date+enrollment
        present_set = set([int(x) for x in (form.present_list.data or "").split(",") if x.strip().isdigit()])
        for e in Enrollment.query.filter_by(course_id=c_id).all():
            # check if record exists for that date; if so, update, else create
            rec = Attendance.query.filter_by(enrollment_id=e.id, att_date=d).first()
            is_present = e.id in present_set
            if rec:
                rec.present = is_present
            else:
                db.session.add(Attendance(enrollment_id=e.id, att_date=d, present=is_present))
        db.session.commit()
        flash("Attendance saved.", "success")
        return redirect(url_for("main.attendance"))
    # GET: list enrolled students helper
    if request.method == "GET":
        c_id = request.args.get("course_id", type=int)
        if c_id:
            enrolled = Enrollment.query.filter_by(course_id=c_id).all()
    courses = Course.query.order_by(Course.id).all()
    return render_template("attendance.html", form=form, courses=courses, enrolled=enrolled)

# Grades
@main.route("/grades", methods=["GET","POST"])
def grades():
    form = GradeForm()
    if form.validate_on_submit():
        c_id = form.course_id.data
        for line in form.lines.data.splitlines():
            if '|' in line:
                eid_s, asmt, score_s = [x.strip() for x in line.split('|',2)]
                eid = int(eid_s); score = float(score_s)
                if not Enrollment.query.get(eid):
                    flash(f"Invalid enrollment id: {eid}", "danger"); return redirect(url_for("main.grades"))
                db.session.add(Grade(enrollment_id=eid, assessment=asmt, score=score))
        db.session.commit()
        flash("Grades saved.", "success")
        return redirect(url_for("main.grades"))
    courses = Course.query.order_by(Course.id).all()
    return render_template("grades.html", form=form, courses=courses)

# Report Card
@main.route("/report", methods=["GET","POST"])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        sid = form.student_id.data
        s = Student.query.get_or_404(sid)
        rows = []
        for e in Enrollment.query.filter_by(student_id=sid).all():
            # attendance %
            total = Attendance.query.filter_by(enrollment_id=e.id).count()
            present = Attendance.query.filter_by(enrollment_id=e.id, present=True).count()
            pct = (present/total*100.0) if total else 0.0
            # average score
            g = Grade.query.filter_by(enrollment_id=e.id).all()
            avg = sum([x.score for x in g])/len(g) if g else 0.0
            rows.append({"course": e.course.name, "teacher": e.teacher.name, "attendance_pct": pct, "avg_score": avg})
        path = report_card(Config.PDF_OUTPUT, s, rows)
        return send_file(path, as_attachment=True)
    students = Student.query.order_by(Student.id).all()
    return render_template("report.html", form=form, students=students)

# Simple APIs to help lookup
@main.route("/api/students")
def api_students():
    items = Student.query.order_by(Student.id).all()
    return jsonify([{"id":s.id,"name":s.name,"roll_no":s.roll_no,"std":s.std} for s in items])

@main.route("/api/courses")
def api_courses():
    items = Course.query.order_by(Course.id).all()
    return jsonify([{"id":c.id,"name":c.name,"code":c.code} for c in items])

app.register_blueprint(main, url_prefix="/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
