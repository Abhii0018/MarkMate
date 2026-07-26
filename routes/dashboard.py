from flask import Blueprint, render_template
from datetime import date
from models.student import Student
from models.attendance import Attendance
from routes import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    today = date.today()
    
    # Calculate statistics
    total_students = Student.query.count()
    present_today = Attendance.query.filter_by(attendance_date=today, status='Present').count()
    absent_today = Attendance.query.filter_by(attendance_date=today, status='Absent').count()
    
    # Fetch recent 5 attendance records
    recent_attendance = Attendance.query.order_by(Attendance.id.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        present_today=present_today,
        absent_today=absent_today,
        today_date=today.strftime('%B %d, %Y'),
        recent_attendance=recent_attendance
    )
