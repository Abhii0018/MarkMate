import os
import socket

def is_mysql_available(host='localhost', port=3306):
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except (socket.error, OverflowError):
        return False

class Config:
    # Secret Key for Flask sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'markmate_secret_key_12345'
    
    # Database Configuration
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'attendance_db')
    
    USE_SQLITE = os.environ.get('USE_SQLITE', 'False').lower() in ['true', '1', 't']
    SQLITE_PATH = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'attendance.db')

    # Automatically check if MySQL is running on port 3306
    if USE_SQLITE or not is_mysql_available(MYSQL_HOST, 3306):
        SQLALCHEMY_DATABASE_URI = SQLITE_PATH
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


