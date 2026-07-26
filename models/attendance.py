from models import db
from datetime import date

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.Enum('Present', 'Absent'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'attendance_date', name='unique_student_date'),
    )

    def __repr__(self):
        return f"<Attendance StudentID={self.student_id} Date={self.attendance_date} Status={self.status}>"
