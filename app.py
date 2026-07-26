from flask import Flask
from config import Config
from models import db
from models.admin import Admin
from models.student import Student
from models.attendance import Attendance
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp
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
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    # Automatically create database tables and seed initial admin user if not present
    with app.app_context():
        db.create_all()

        # Seed default admin if table is empty
        if not Admin.query.filter_by(username='admin').first():
            default_admin = Admin(username='admin')
            default_admin.set_password('admin123')
            db.session.add(default_admin)
            
            # Seed sample students if empty
            if Student.query.count() == 0:
                s1 = Student(roll_number='CS101', name='Rahul Sharma', department='Computer Science', semester='Semester 6')
                s2 = Student(roll_number='CS102', name='Priya Patel', department='Computer Science', semester='Semester 6')
                s3 = Student(roll_number='IT101', name='Amit Kumar', department='Information Technology', semester='Semester 4')
                s4 = Student(roll_number='EC101', name='Sneha Gupta', department='Electronics', semester='Semester 4')
                s5 = Student(roll_number='ME101', name='Vikram Singh', department='Mechanical', semester='Semester 2')
                db.session.add_all([s1, s2, s3, s4, s5])
                
            db.session.commit()



    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

