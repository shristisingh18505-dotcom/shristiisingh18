from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class StudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    roll_no = StringField("Roll No", validators=[DataRequired(), Length(max=50)])
    std = StringField("Class/Section", validators=[Optional()])
    dob = StringField("DOB", validators=[Optional()])
    submit = SubmitField("Save")

class TeacherForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    subject = StringField("Subject", validators=[Optional()])
    submit = SubmitField("Save")

class CourseForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    code = StringField("Code", validators=[DataRequired()])
    submit = SubmitField("Save")

class EnrollForm(FlaskForm):
    student_id = IntegerField("Student ID", validators=[DataRequired()])
    course_id = IntegerField("Course ID", validators=[DataRequired()])
    teacher_id = IntegerField("Teacher ID", validators=[DataRequired()])
    submit = SubmitField("Enroll")

class AttendanceForm(FlaskForm):
    course_id = IntegerField("Course ID", validators=[DataRequired()])
    att_date = DateField("Date", validators=[DataRequired()])
    # students present as "enrollment_id,enrollment_id,..."
    present_list = StringField("Present Enrollment IDs (comma-separated)", validators=[Optional()])
    submit = SubmitField("Save Attendance")

class GradeForm(FlaskForm):
    course_id = IntegerField("Course ID", validators=[DataRequired()])
    lines = TextAreaField("Grades (one per line: enrollment_id|assessment|score)", validators=[DataRequired()])
    submit = SubmitField("Save Grades")

class ReportForm(FlaskForm):
    student_id = IntegerField("Student ID", validators=[DataRequired()])
    submit = SubmitField("Generate Report Card")
