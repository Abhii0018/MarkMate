from models import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

    # Relationship with Attendance model
    attendances = db.relationship('Attendance', backref='student', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Student {self.roll_number} - {self.name}>"
