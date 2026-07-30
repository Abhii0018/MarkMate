from flask import Flask
from datetime import date, timedelta
from config import Config
from models import db
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.attendance import Attendance

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp
from routes.teachers import teachers_bp
from routes.teacher import teacher_bp
from routes.student_portal import student_bp
from routes.attendance import attendance_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(teachers_bp, url_prefix='/teachers')
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    # Automatically create database tables and seed initial data
    with app.app_context():
        db.create_all()

        # 1. Seed default Admin if not present
        if not Admin.query.filter_by(username='admin').first():
            default_admin = Admin(username='admin')
            default_admin.set_password('admin123')
            db.session.add(default_admin)
            db.session.commit()

        # 2. Seed default Teachers for Civil, Mechanical, Computer Science if empty or < 3
        if Teacher.query.count() < 3:
            sample_teachers = [
                Teacher(username='prof.sharma', name='Prof. Rajesh Sharma', department='Computer Science', email='sharma@markmate.edu'),
                Teacher(username='prof.verma', name='Prof. Suresh Verma', department='Mechanical', email='verma@markmate.edu'),
                Teacher(username='prof.gupta', name='Prof. Ananya Gupta', department='Civil', email='gupta@markmate.edu'),
                Teacher(username='prof.singh', name='Prof. Vikram Singh', department='Computer Science', email='singh@markmate.edu')
            ]
            for t in sample_teachers:
                if not Teacher.query.filter_by(username=t.username).first():
                    t.set_password('teacher123')
                    db.session.add(t)
            db.session.commit()

        # 3. Seed Students with passwords if count < 10
        if Student.query.count() < 10:
            Student.query.delete()
            db.session.commit()
            
            sample_students = [
                Student(roll_number='CS101', name='Rahul Sharma', department='Computer Science', semester='Semester 6'),
                Student(roll_number='CS102', name='Priya Patel', department='Computer Science', semester='Semester 6'),
                Student(roll_number='CS103', name='Rohan Verma', department='Computer Science', semester='Semester 6'),
                Student(roll_number='IT101', name='Amit Kumar', department='Information Technology', semester='Semester 4'),
                Student(roll_number='IT102', name='Neha Singh', department='Information Technology', semester='Semester 4'),
                Student(roll_number='EC101', name='Sneha Gupta', department='Electronics', semester='Semester 4'),
                Student(roll_number='EC102', name='Ankit Yadav', department='Electronics', semester='Semester 4'),
                Student(roll_number='ME101', name='Vikram Singh', department='Mechanical', semester='Semester 2'),
                Student(roll_number='ME102', name='Karan Malhotra', department='Mechanical', semester='Semester 2'),
                Student(roll_number='CE101', name='Pooja Roy', department='Civil', semester='Semester 4'),
                Student(roll_number='CE102', name='Deepak Mishra', department='Civil', semester='Semester 4'),
                Student(roll_number='EE101', name='Siddharth Rao', department='Electrical', semester='Semester 6'),
                Student(roll_number='EE102', name='Divya Joshi', department='Electrical', semester='Semester 6'),
                Student(roll_number='CS104', name='Aarav Mehta', department='Computer Science', semester='Semester 2'),
                Student(roll_number='IT103', name='Isha Nair', department='Information Technology', semester='Semester 2')
            ]
            for s in sample_students:
                s.set_password('student123')
                db.session.add(s)
            db.session.commit()

        # 4. Seed Historical Attendance across 6 dates to ensure clear threshold demo (e.g. CS103 & ME102 < 75%)
        today = date.today()
        past_dates = [today - timedelta(days=i) for i in range(5, -1, -1)]

        low_attendance_rolls = {'CS103', 'ME102', 'CE101'} # These will have < 75% attendance

        for d in past_dates:
            for student in Student.query.all():
                existing = Attendance.query.filter_by(student_id=student.id, attendance_date=d).first()
                if not existing:
                    if student.roll_number in low_attendance_rolls:
                        # Absent on most days -> attendance around 33% - 50% (< 75%)
                        status = 'Present' if (d.day % 3 == 0) else 'Absent'
                    else:
                        # Present on most days -> attendance around 83% - 100% (>= 75%)
                        status = 'Absent' if (d.day % 7 == 0) else 'Present'
                    db.session.add(Attendance(student_id=student.id, attendance_date=d, status=status))

        db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
