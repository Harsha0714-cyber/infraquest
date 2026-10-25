CREATE DATABASE IF NOT EXISTS infrastructure_db;
USE infrastructure_db;

CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    issue VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    department VARCHAR(100) NOT NULL,
    complaint_date DATE NOT NULL
);
