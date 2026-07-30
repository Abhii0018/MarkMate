from flask import Blueprint, render_template, send_from_directory, current_app
from datetime import date
import os
from models.student import Student
from models.attendance import Attendance
from routes import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def landing():
    return render_template('landing.html')

@dashboard_bp.route('/download-ppt')
def download_ppt():
    directory = current_app.root_path
    filename = 'MarkMate_Project_Presentation.pptx'
    return send_from_directory(directory, filename, as_attachment=True)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()
    
    # Calculate statistics
    total_students = Student.query.count()
    present_today = Attendance.query.filter_by(attendance_date=today, status='Present').count()
    absent_today = Attendance.query.filter_by(attendance_date=today, status='Absent').count()
    
    # Overall attendance rate percentage
    total_marked_today = present_today + absent_today
    attendance_rate = round((present_today / total_marked_today * 100), 1) if total_marked_today > 0 else 0.0

    # Fetch recent 5 attendance records
    recent_attendance = Attendance.query.order_by(Attendance.id.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        present_today=present_today,
        absent_today=absent_today,
        attendance_rate=attendance_rate,
        today_date=today.strftime('%B %d, %Y'),
        recent_attendance=recent_attendance
    )

