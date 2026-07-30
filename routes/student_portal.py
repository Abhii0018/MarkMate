from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.student import Student
from models.attendance import Attendance
from routes import student_required

student_bp = Blueprint('student_portal', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@student_required
def dashboard():
    student_id = session.get('student_id')
    student = Student.query.get_or_404(student_id)

    # Fetch all attendance records for this student
    attendance_records = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.attendance_date.desc()).all()

    total_classes = len(attendance_records)
    present_count = sum(1 for r in attendance_records if r.status == 'Present')
    absent_count = sum(1 for r in attendance_records if r.status == 'Absent')

    if total_classes > 0:
        overall_percentage = round((present_count / total_classes) * 100, 1)
    else:
        overall_percentage = 0.0

    is_below_threshold = overall_percentage < 75.0

    return render_template(
        'student/dashboard.html',
        student=student,
        attendance_records=attendance_records,
        total_classes=total_classes,
        present_count=present_count,
        absent_count=absent_count,
        overall_percentage=overall_percentage,
        is_below_threshold=is_below_threshold
    )
