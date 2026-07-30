-- =================================================
-- MarkMate Expanded Database Script
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
-- Table structure for `teachers`
-- -------------------------------------------------
CREATE TABLE IF NOT EXISTS `teachers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) DEFAULT NULL,
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
    `password` VARCHAR(255) DEFAULT NULL,
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
-- Seed Admin
-- -------------------------------------------------
INSERT INTO `admins` (`username`, `password`) VALUES
('admin', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d')
ON DUPLICATE KEY UPDATE `username`=`username`;

-- -------------------------------------------------
-- Seed Teachers (Civil, Mechanical, Computer Science)
-- -------------------------------------------------
INSERT INTO `teachers` (`username`, `password`, `name`, `department`, `email`) VALUES
('prof.sharma', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d', 'Prof. Rajesh Sharma', 'Computer Science', 'sharma@markmate.edu'),
('prof.verma', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d', 'Prof. Suresh Verma', 'Mechanical', 'verma@markmate.edu'),
('prof.gupta', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d', 'Prof. Ananya Gupta', 'Civil', 'gupta@markmate.edu'),
('prof.singh', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d', 'Prof. Vikram Singh', 'Computer Science', 'singh@markmate.edu')
ON DUPLICATE KEY UPDATE `username`=`username`;

-- -------------------------------------------------
-- Seed Students
-- -------------------------------------------------
INSERT INTO `students` (`roll_number`, `name`, `department`, `semester`, `password`) VALUES
('CS101', 'Rahul Sharma', 'Computer Science', 'Semester 6', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('CS102', 'Priya Patel', 'Computer Science', 'Semester 6', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('CS103', 'Rohan Verma', 'Computer Science', 'Semester 6', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('IT101', 'Amit Kumar', 'Information Technology', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('IT102', 'Neha Singh', 'Information Technology', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('EC101', 'Sneha Gupta', 'Electronics', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('EC102', 'Ankit Yadav', 'Electronics', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('ME101', 'Vikram Singh', 'Mechanical', 'Semester 2', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('ME102', 'Karan Malhotra', 'Mechanical', 'Semester 2', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('CE101', 'Pooja Roy', 'Civil', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('CE102', 'Deepak Mishra', 'Civil', 'Semester 4', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('EE101', 'Siddharth Rao', 'Electrical', 'Semester 6', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('EE102', 'Divya Joshi', 'Electrical', 'Semester 6', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('CS104', 'Aarav Mehta', 'Computer Science', 'Semester 2', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d'),
('IT103', 'Isha Nair', 'Information Technology', 'Semester 2', 'scrypt:32768:8:1$uH3jJ2fO9XyqL2vE$e7b51f0436d44558bc1a43a8ce7c3b2cb1e360f796d8ddb5bfcf5ec0005db37911b369fb04c6ff2bd44b02ba14ce42d76feccecb547796d8e82ef6ff7e868a2d')
ON DUPLICATE KEY UPDATE `roll_number`=`roll_number`;
