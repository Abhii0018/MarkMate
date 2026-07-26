import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from datetime import date, datetime
from models import db
from models.student import Student
from models.attendance import Attendance
from routes import login_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    # Allow custom selected date, defaulting to today
    selected_date_str = request.args.get('date', '').strip()
    if selected_date_str:
        try:
            target_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    students = Student.query.order_by(Student.roll_number.asc()).all()

    if request.method == 'POST':
        date_param = request.form.get('attendance_date', '').strip()
        if date_param:
            try:
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                pass

        saved_count = 0
        duplicate_count = 0

        for student in students:
            status = request.form.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    attendance_date=target_date
                ).first()

                if existing:
                    existing.status = status
                    duplicate_count += 1
                else:
                    new_attendance = Attendance(
                        student_id=student.id,
                        attendance_date=target_date,
                        status=status
                    )
                    db.session.add(new_attendance)
                    saved_count += 1

        db.session.commit()
        flash(f'Attendance successfully recorded for {target_date.strftime("%B %d, %Y")}!', 'success')
        return redirect(url_for('attendance.attendance_records', date=target_date.strftime('%Y-%m-%d')))

    # Existing records for target date
    target_records = {a.student_id: a.status for a in Attendance.query.filter_by(attendance_date=target_date).all()}

    return render_template(
        'attendance/mark.html',
        students=students,
        target_date=target_date,
        target_records=target_records
    )

@attendance_bp.route('/export')
@login_required
def export_csv():
    records = Attendance.query.join(Student).order_by(Attendance.attendance_date.desc(), Student.roll_number.asc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Roll Number', 'Student Name', 'Department', 'Semester', 'Status'])

    for record in records:
        writer.writerow([
            record.attendance_date.strftime('%Y-%m-%d'),
            record.student.roll_number,
            record.student.name,
            record.student.department,
            record.student.semester,
            record.status
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=attendance_records_export.csv"}
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
