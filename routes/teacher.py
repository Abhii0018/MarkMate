from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date, datetime
from models import db
from models.teacher import Teacher
from models.student import Student
from models.attendance import Attendance
from routes import teacher_required

teacher_bp = Blueprint('teacher_portal', __name__, url_prefix='/teacher')

@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    teacher_id = session.get('teacher_id')
    teacher = Teacher.query.get(teacher_id)
    dept = teacher.department if teacher else session.get('department')
    today = date.today()

    # Department students
    students = Student.query.filter_by(department=dept).all()
    total_students = len(students)
    student_ids = [s.id for s in students]

    # Department today's attendance metrics
    if student_ids:
        present_today = Attendance.query.filter(
            Attendance.student_id.in_(student_ids),
            Attendance.attendance_date == today,
            Attendance.status == 'Present'
        ).count()

        absent_today = Attendance.query.filter(
            Attendance.student_id.in_(student_ids),
            Attendance.attendance_date == today,
            Attendance.status == 'Absent'
        ).count()
    else:
        present_today = 0
        absent_today = 0

    total_marked = present_today + absent_today
    attendance_rate = round((present_today / total_marked * 100), 1) if total_marked > 0 else 0.0

    # Recent attendance for this department
    recent_attendance = []
    if student_ids:
        recent_attendance = Attendance.query.filter(
            Attendance.student_id.in_(student_ids)
        ).order_by(Attendance.attendance_date.desc(), Attendance.id.desc()).limit(10).all()

    return render_template(
        'teacher/dashboard.html',
        teacher=teacher,
        department=dept,
        students=students,
        total_students=total_students,
        present_today=present_today,
        absent_today=absent_today,
        attendance_rate=attendance_rate,
        today_date=today.strftime('%B %d, %Y'),
        recent_attendance=recent_attendance
    )

@teacher_bp.route('/mark-attendance', methods=['GET', 'POST'])
@teacher_required
def mark_attendance():
    dept = session.get('department')
    students = Student.query.filter_by(department=dept).order_by(Student.roll_number).all()

    selected_date_str = request.form.get('attendance_date') or request.args.get('date') or date.today().isoformat()
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()

    if request.method == 'POST' and 'submit_attendance' in request.form:
        for student in students:
            status = request.form.get(f'status_{student.id}', 'Absent')
            existing_record = Attendance.query.filter_by(
                student_id=student.id,
                attendance_date=selected_date
            ).first()

            if existing_record:
                existing_record.status = status
            else:
                new_record = Attendance(
                    student_id=student.id,
                    attendance_date=selected_date,
                    status=status
                )
                db.session.add(new_record)

        db.session.commit()
        flash(f'Attendance recorded successfully for {dept} department on {selected_date.strftime("%B %d, %Y")}!', 'success')
        return redirect(url_for('teacher_portal.mark_attendance', date=selected_date.isoformat()))

    # Existing attendance map for rendering
    attendance_map = {}
    if students:
        student_ids = [s.id for s in students]
        records = Attendance.query.filter(
            Attendance.student_id.in_(student_ids),
            Attendance.attendance_date == selected_date
        ).all()
        for r in records:
            attendance_map[r.student_id] = r.status

    return render_template(
        'teacher/mark.html',
        students=students,
        department=dept,
        selected_date=selected_date,
        attendance_map=attendance_map
    )

@teacher_bp.route('/records')
@teacher_required
def records():
    dept = session.get('department')
    students = Student.query.filter_by(department=dept).all()
    student_ids = [s.id for s in students]

    filter_date = request.args.get('date', '').strip()
    query = Attendance.query.filter(Attendance.student_id.in_(student_ids)) if student_ids else Attendance.query.filter(False)

    if filter_date:
        try:
            d_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            query = query.filter_by(attendance_date=d_obj)
        except ValueError:
            pass

    records = query.order_by(Attendance.attendance_date.desc(), Attendance.id.desc()).all()

    return render_template('teacher/records.html', records=records, department=dept, filter_date=filter_date)
