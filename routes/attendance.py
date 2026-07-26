from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from models import db
from models.student import Student
from models.attendance import Attendance
from routes import login_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    today = date.today()
    students = Student.query.order_by(Student.roll_number.asc()).all()

    if request.method == 'POST':
        # Get selected status for each student
        saved_count = 0
        duplicate_count = 0

        for student in students:
            status = request.form.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                # Check if duplicate record exists for today
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    attendance_date=today
                ).first()

                if existing:
                    # Update status if already present or flag duplicate
                    existing.status = status
                    duplicate_count += 1
                else:
                    new_attendance = Attendance(
                        student_id=student.id,
                        attendance_date=today,
                        status=status
                    )
                    db.session.add(new_attendance)
                    saved_count += 1

        db.session.commit()
        
        if duplicate_count > 0 and saved_count == 0:
            flash("Attendance Updated Successfully for Today's Students!", 'info')
        else:
            flash('Attendance Saved Successfully!', 'success')
            
        return redirect(url_for('attendance.attendance_records'))

    # Check today's existing attendance status to pre-select radio buttons if available
    today_records = {a.student_id: a.status for a in Attendance.query.filter_by(attendance_date=today).all()}

    return render_template(
        'attendance/mark.html',
        students=students,
        today_date=today,
        today_records=today_records
    )

@attendance_bp.route('/records')
@login_required
def attendance_records():
    search_query = request.args.get('q', '').strip()
    date_query = request.args.get('date', '').strip()

    query = Attendance.query.join(Student)

    if search_query:
        query = query.filter(
            (Student.name.ilike(f"%{search_query}%")) | 
            (Student.roll_number.ilike(f"%{search_query}%"))
        )

    if date_query:
        try:
            parsed_date = datetime.strptime(date_query, '%Y-%m-%d').date()
            query = query.filter(Attendance.attendance_date == parsed_date)
        except ValueError:
            flash('Invalid date format used for filter.', 'warning')

    records = query.order_by(Attendance.attendance_date.desc(), Student.roll_number.asc()).all()

    return render_template(
        'attendance/records.html',
        records=records,
        search_query=search_query,
        date_query=date_query
    )
