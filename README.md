# Community Infrastructure Problem Analyzer

A Python and MySQL-based application for organizing, analyzing, and reporting community infrastructure complaints such as damaged roads, drainage issues, water supply problems, and streetlight failures.

## Features
- Add new complaints
- Display all complaint records
- Generate location-wise reports
- Generate issue-wise reports
- Produce department-wise and status-wise summaries
- Identify recurring problems
- View open complaints
- Highlight high-priority locations
- Generate a complete infrastructure report

## Project Objective
The application helps convert public complaints into structured records and provides analysis based on:
- Location
- Issue type
- Responsible department
- Status of the complaint

## Tech Stack
- Python 3
- MySQL
- mysql-connector-python

## Setup

1. Install Python dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Create the MySQL database and table

   Open MySQL and run the SQL commands in `database_setup.sql`.

3. Update the database credentials in `app.py`

   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="root",
       password="your_password",
       database="infrastructure_db"
   )
   ```

4. Run the app

   ```bash
   python app.py
   ```

## File Structure
- `app.py` - main application logic
- `database_setup.sql` - database and table creation script
- `requirements.txt` - Python package dependencies

## MySQL Database Structure
The application expects a database named `infrastructure_db` with a table named `complaints`.

## Example Menu Options
1. Add Complaint
2. Display All Complaints
3. Location-wise Report
4. Issue-wise Report
5. Department-wise Report
6. Status-wise Report
7. Find Recurring Problems
8. Open Complaints
9. High Priority Locations
10. Generate Complete Report
11. Exit

## Note
The project uses a hardcoded MySQL connection in `app.py`. For production use, it is better to move credentials into environment variables.
