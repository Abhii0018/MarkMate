-- =================================================
-- MarkMate Database Creation Script
-- Database: attendance_db
-- =================================================

CREATE DATABASE IF NOT EXISTS `attendance_db`;
USE `attendance_db`;

-- -------------------------------------------------
-- Table structure for `admins`
-- -------------------------------------------------
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------
-- Table structure for `students`
-- -------------------------------------------------
CREATE TABLE IF NOT EXISTS `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `roll_number` VARCHAR(30) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `semester` VARCHAR(20) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------
-- Table structure for `attendance`
-- -------------------------------------------------
CREATE TABLE IF NOT EXISTS `attendance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `attendance_date` DATE NOT NULL,
    `status` ENUM('Present', 'Absent') NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_student_date` (`student_id`, `attendance_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------
-- Seed Initial Data
-- Default Admin: admin / admin123
-- Password hash generated using Werkzeug scrypt/pbkdf2
-- -------------------------------------------------

INSERT INTO `admins` (`username`, `password`) VALUES
('admin', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d')
ON DUPLICATE KEY UPDATE `username`=`username`;

-- Sample Students
INSERT INTO `students` (`roll_number`, `name`, `department`, `semester`) VALUES
('CS101', 'Rahul Sharma', 'Computer Science', 'Semester 6'),
('CS102', 'Priya Patel', 'Computer Science', 'Semester 6'),
('IT101', 'Amit Kumar', 'Information Technology', 'Semester 4'),
('EC101', 'Sneha Gupta', 'Electronics', 'Semester 4'),
('ME101', 'Vikram Singh', 'Mechanical', 'Semester 2')
ON DUPLICATE KEY UPDATE `roll_number`=`roll_number`;
