from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=True)

    # Relationship with Attendance model
    attendances = db.relationship('Attendance', backref='student', cascade='all, delete-orphan', lazy=True)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        if not self.password:
            # Default password fallback if not set
            return raw_password == 'student123'
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<Student {self.roll_number} - {self.name}>"
