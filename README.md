# MarkMate - Student Attendance Management System

**MarkMate** is a clean, modern, beginner-friendly full-stack web application designed for student attendance management. Built with Flask, SQLAlchemy, MySQL, and Bootstrap 5, it is well-structured and easy to explain during a college mini project viva.

---

## 🚀 Features

- **Admin Authentication**: Secure login/logout using Werkzeug password hashing.
- **Dashboard Overview**: Metrics displaying Total Students, Present Today, Absent Today, Today's Date, and recent attendance logs.
- **Student Management (CRUD)**:
  - Add new student with unique roll numbers.
  - Edit existing student details.
  - Delete student with modal popup confirmation.
  - Search students by Roll Number or Name.
- **Mark Attendance**:
  - Automatically selects today's date.
  - Interactive radio toggles for Present / Absent status.
  - Prevents duplicate attendance entries per date.
- **Attendance Records**:
  - Filter attendance history by student name, roll number, or date.
  - Visual status indicators with Bootstrap Badges (Green = Present, Red = Absent).

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, SQLAlchemy, Flask Blueprints
- **Database**: MySQL (PyMySQL) / SQLite (Fallback option)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons, JavaScript

---

## 📁 Folder Structure

```text
attendance_system/
│── app.py                # Main Flask application entry point
│── config.py             # Database and app configurations
│── requirements.txt      # Project dependencies
│── README.md             # Documentation & Viva setup guide
│── database.sql          # MySQL database export & seed script
│
│── models/               # SQLAlchemy Models
│   ├── __init__.py
│   ├── admin.py
│   ├── student.py
│   └── attendance.py
│
│── routes/               # Flask Blueprints / Modular Routes
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── students.py
│   └── attendance.py
│
│── templates/            # Jinja2 HTML Templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   └── attendance/
│       ├── mark.html
│       └── records.html
│
└── static/               # Static Web Assets
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
Make sure Python 3.8+ and MySQL Server are installed on your machine.

### 2. Set Up MySQL Database
1. Open your MySQL terminal or phpMyAdmin.
2. Run the provided SQL script:
   ```bash
   mysql -u root -p < database.sql
   ```
   *(Or import `database.sql` directly inside phpMyAdmin).*

### 3. Install Python Dependencies
Create a virtual environment (optional) and install requirements:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 💡 Quick Test / SQLite Option
If MySQL server is not installed locally, set `USE_SQLITE=True` in environment variables or `config.py`. The app will automatically initialize SQLite and seed initial admin & student data upon execution!

---

## 🔑 Default Admin Login Credentials

- **Username**: `admin`
- **Password**: `admin123`
