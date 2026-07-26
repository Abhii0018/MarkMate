from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.student import Student
from routes import login_required

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
@login_required
def list_students():
    query = request.args.get('q', '').strip()
    if query:
        # Search by Roll Number or Name
        students = Student.query.filter(
            (Student.roll_number.ilike(f"%{query}%")) | 
            (Student.name.ilike(f"%{query}%"))
        ).all()
    else:
        students = Student.query.order_by(Student.id.desc()).all()
        
    return render_template('students/list.html', students=students, query=query)

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()

        # Validation
        if not roll_number or not name or not department or not semester:
            flash('All fields are required.', 'warning')
            return render_template('students/add.html')

        # Check unique roll number
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            flash(f'Student with Roll Number "{roll_number}" already exists!', 'danger')
            return render_template('students/add.html')

        new_student = Student(
            roll_number=roll_number,
            name=name,
            department=department,
            semester=semester
        )
        db.session.add(new_student)
        db.session.commit()

        flash('Student Added Successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/add.html')

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()

        # Validation
        if not roll_number or not name or not department or not semester:
            flash('All fields are required.', 'warning')
            return render_template('students/edit.html', student=student)

        # Check unique roll number excluding current student
        existing = Student.query.filter(Student.roll_number == roll_number, Student.id != id).first()
        if existing:
            flash(f'Student with Roll Number "{roll_number}" already exists!', 'danger')
            return render_template('students/edit.html', student=student)

        student.roll_number = roll_number
        student.name = name
        student.department = department
        student.semester = semester

        db.session.commit()
        flash('Student Updated Successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit.html', student=student)

@students_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student Deleted Successfully!', 'success')
    return redirect(url_for('students.list_students'))
