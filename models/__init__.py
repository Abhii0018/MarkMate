from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.attendance import Attendance
