from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to respective dashboard
    if session.get('user_type') == 'admin' or 'admin_id' in session:
        return redirect(url_for('dashboard.index'))
    elif session.get('user_type') == 'teacher':
        return redirect(url_for('teacher_portal.dashboard'))
    elif session.get('user_type') == 'student':
        return redirect(url_for('student_portal.dashboard'))

    active_tab = request.args.get('role', 'admin')

    if request.method == 'POST':
        role = request.form.get('role', 'admin').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        active_tab = role

        if not username or not password:
            flash('Please fill in all required fields.', 'warning')
            return render_template('login.html', active_tab=active_tab)

        if role == 'admin':
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                session.clear()
                session['user_type'] = 'admin'
                session['admin_id'] = admin.id
                session['username'] = admin.username
                flash(f'Welcome Admin ({admin.username})!', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Invalid Admin username or password.', 'danger')

        elif role == 'teacher':
            teacher = Teacher.query.filter_by(username=username).first()
            if teacher and teacher.check_password(password):
                session.clear()
                session['user_type'] = 'teacher'
                session['teacher_id'] = teacher.id
                session['username'] = teacher.username
                session['name'] = teacher.name
                session['department'] = teacher.department
                flash(f'Welcome Prof. {teacher.name} ({teacher.department})!', 'success')
                return redirect(url_for('teacher_portal.dashboard'))
            else:
                flash('Invalid Teacher username or password.', 'danger')

        elif role == 'student':
            student = Student.query.filter_by(roll_number=username.upper()).first()
            if student and student.check_password(password):
                session.clear()
                session['user_type'] = 'student'
                session['student_id'] = student.id
                session['roll_number'] = student.roll_number
                session['name'] = student.name
                session['department'] = student.department
                flash(f'Welcome {student.name} ({student.roll_number})!', 'success')
                return redirect(url_for('student_portal.dashboard'))
            else:
                flash('Invalid Roll Number or Student password.', 'danger')

    return render_template('login.html', active_tab=active_tab)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
