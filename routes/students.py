from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.student import Student
from models.attendance import Attendance
from routes import admin_required

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
@admin_required
def list_students():
    query_str = request.args.get('q', '').strip()
    selected_dept = request.args.get('department', '').strip()

    student_query = Student.query

    if selected_dept and selected_dept != 'All':
        student_query = student_query.filter_by(department=selected_dept)

    if query_str:
        student_query = student_query.filter(
            (Student.roll_number.ilike(f"%{query_str}%")) | 
            (Student.name.ilike(f"%{query_str}%"))
        )

    students = student_query.order_by(Student.roll_number.asc()).all()
        
    # Calculate attendance statistics for each student
    student_stats = []
    for s in students:
        total = Attendance.query.filter_by(student_id=s.id).count()
        present = Attendance.query.filter_by(student_id=s.id, status='Present').count()
        percentage = round((present / total * 100), 1) if total > 0 else 0.0
        student_stats.append({
            'student': s,
            'total': total,
            'present': present,
            'percentage': percentage
        })

    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']

    return render_template(
        'students/list.html',
        student_stats=student_stats,
        query=query_str,
        selected_dept=selected_dept,
        departments=departments
    )


@students_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()
        password = request.form.get('password', '').strip() or 'student123'

        if not roll_number or not name or not department or not semester:
            flash('All fields are required.', 'warning')
            return render_template('students/add.html', departments=departments)

        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            flash(f'Student with Roll Number "{roll_number}" already exists!', 'danger')
            return render_template('students/add.html', departments=departments)

        new_student = Student(
            roll_number=roll_number,
            name=name,
            department=department,
            semester=semester
        )
        new_student.set_password(password)

        db.session.add(new_student)
        db.session.commit()

        flash('Student Added Successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/add.html', departments=departments)

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']

    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()
        new_password = request.form.get('password', '').strip()

        if not roll_number or not name or not department or not semester:
            flash('All fields are required.', 'warning')
            return render_template('students/edit.html', student=student, departments=departments)

        existing = Student.query.filter(Student.roll_number == roll_number, Student.id != id).first()
        if existing:
            flash(f'Student with Roll Number "{roll_number}" already exists!', 'danger')
            return render_template('students/edit.html', student=student, departments=departments)

        student.roll_number = roll_number
        student.name = name
        student.department = department
        student.semester = semester

        if new_password:
            student.set_password(new_password)

        db.session.commit()
        flash('Student Updated Successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit.html', student=student, departments=departments)

@students_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student Deleted Successfully!', 'success')
    return redirect(url_for('students.list_students'))
