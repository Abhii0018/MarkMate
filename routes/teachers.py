from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.teacher import Teacher
from routes import admin_required

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/')
@admin_required
def list_teachers():
    selected_dept = request.args.get('department', '').strip()
    
    query = Teacher.query
    if selected_dept and selected_dept != 'All':
        query = query.filter_by(department=selected_dept)
        
    teachers = query.order_by(Teacher.department, Teacher.name).all()
    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']
    
    return render_template('teachers/list.html', teachers=teachers, selected_dept=selected_dept, departments=departments)

@teachers_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_teacher():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not name or not department or not password:
            flash('Username, Name, Department, and Password are required.', 'warning')
            return render_template('teachers/add.html')

        if Teacher.query.filter_by(username=username).first():
            flash(f'Teacher username "{username}" already exists.', 'danger')
            return render_template('teachers/add.html')

        teacher = Teacher(
            username=username,
            name=name,
            department=department,
            email=email
        )
        teacher.set_password(password)

        db.session.add(teacher)
        db.session.commit()
        flash(f'Teacher "{name}" added successfully for {department} department!', 'success')
        return redirect(url_for('teachers.list_teachers'))

    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']
    return render_template('teachers/add.html', departments=departments)

@teachers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        teacher.name = request.form.get('name', '').strip()
        teacher.department = request.form.get('department', '').strip()
        teacher.email = request.form.get('email', '').strip()
        new_password = request.form.get('password', '').strip()

        if new_password:
            teacher.set_password(new_password)

        db.session.commit()
        flash(f'Teacher "{teacher.name}" updated successfully.', 'success')
        return redirect(url_for('teachers.list_teachers'))

    departments = ['Computer Science', 'Mechanical', 'Civil', 'Information Technology', 'Electronics', 'Electrical']
    return render_template('teachers/edit.html', teacher=teacher, departments=departments)

@teachers_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    name = teacher.name
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Teacher "{name}" deleted successfully.', 'success')
    return redirect(url_for('teachers.list_teachers'))
