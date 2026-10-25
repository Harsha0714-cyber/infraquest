import mysql.connector
from datetime import date


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def connect_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chintu@27",
            database="infrastructure_db"
        )

        print("\nDatabase connected successfully!")
        return conn

    except mysql.connector.Error as e:
        print("\nDatabase connection failed!")
        print("Error:", e)
        return None


# ==========================================================
# CATEGORIZE COMPLAINT
# ==========================================================

def categorize_issue(description):

    text = description.lower()

    # Drainage
    if (
        "drain" in text
        or "drainage" in text
        or "sewage" in text
        or "sewer" in text
        or "overflow" in text
        or "waterlogging" in text
    ):
        return "Drainage"

    # Water Supply
    elif (
        "water supply" in text
        or "water pipeline" in text
        or "water pipe" in text
        or "tap" in text
        or "no water" in text
        or "pipeline" in text
    ):
        return "Water Supply"

    # Streetlights
    elif (
        "streetlight" in text
        or "street light" in text
        or "street lamp" in text
        or "lamp" in text
        or "lighting" in text
        or "light not working" in text
    ):
        return "Streetlights"

    # Roads
    elif (
        "pothole" in text
        or "road damage" in text
        or "damaged road" in text
        or "road" in text
        or "footpath" in text
        or "pavement" in text
    ):
        return "Roads"

    # Other
    else:
        return "Other Infrastructure"

# ==========================================================
# CALCULATE PRIORITY
# ==========================================================

def calculate_priority(count):

    if count >= 16:
        return "HIGH"

    elif count >= 6:
        return "MEDIUM"

    else:
        return "LOW"


# ==========================================================
# ADD COMPLAINT
# ==========================================================

def add_complaint(conn):

    print("\n========== ADD NEW COMPLAINT ==========")

    location = input("Enter location/ward: ")

    description = input("Enter complaint description: ")

    status = input(
        "Enter status (Open/Closed/Pending): "
    )

    department = input(
        "Enter responsible department: "
    )

    issue = categorize_issue(description)

    cursor = conn.cursor()

    sql = """
    INSERT INTO complaints
    (
        location,
        issue,
        description,
        status,
        department,
        complaint_date
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        location,
        issue,
        description,
        status,
        department,
        date.today()
    )

    cursor.execute(sql, values)

    conn.commit()

    print("\nComplaint added successfully!")
    print("Automatically detected category:", issue)

    cursor.close()


# ==========================================================
# DISPLAY ALL COMPLAINTS
# ==========================================================

def display_complaints(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            complaint_id,
            location,
            issue,
            description,
            status,
            department,
            complaint_date
        FROM complaints
        ORDER BY complaint_id
    """)

    records = cursor.fetchall()

    print("\n========== ALL COMPLAINTS ==========")

    if len(records) == 0:

        print("No complaints found.")

    else:

        for row in records:

            print("------------------------------------------")

            print("Complaint ID :", row[0])
            print("Location     :", row[1])
            print("Issue        :", row[2])
            print("Description  :", row[3])
            print("Status       :", row[4])
            print("Department   :", row[5])
            print("Date         :", row[6])

    cursor.close()


# ==========================================================
# LOCATION-WISE ANALYSIS
# ==========================================================

def location_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            location,
            COUNT(*) AS complaint_count
        FROM complaints
        GROUP BY location
        ORDER BY complaint_count DESC
    """)

    records = cursor.fetchall()

    print("\n========== LOCATION-WISE REPORT ==========")

    if len(records) == 0:

        print("No complaint data available.")

    else:

        for row in records:

            location = row[0]
            count = row[1]

            priority = calculate_priority(count)

            print("------------------------------------------")
            print("Location         :", location)
            print("Complaint Count  :", count)
            print("Priority         :", priority)

    cursor.close()


# ==========================================================
# ISSUE-WISE ANALYSIS
# ==========================================================

def issue_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            issue,
            COUNT(*) AS issue_count
        FROM complaints
        GROUP BY issue
        ORDER BY issue_count DESC
    """)

    records = cursor.fetchall()

    print("\n========== ISSUE-WISE REPORT ==========")

    if len(records) == 0:

        print("No complaint data available.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Issue           :", row[0])
            print("Complaint Count :", row[1])

    cursor.close()


# ==========================================================
# DEPARTMENT-WISE ANALYSIS
# ==========================================================

def department_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            department,
            COUNT(*) AS complaint_count
        FROM complaints
        GROUP BY department
        ORDER BY complaint_count DESC
    """)

    records = cursor.fetchall()

    print("\n========== DEPARTMENT-WISE REPORT ==========")

    if len(records) == 0:

        print("No complaint data available.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Department      :", row[0])
            print("Complaint Count :", row[1])

    cursor.close()


# ==========================================================
# STATUS-WISE ANALYSIS
# ==========================================================

def status_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*) AS status_count
        FROM complaints
        GROUP BY status
        ORDER BY status_count DESC
    """)

    records = cursor.fetchall()

    print("\n========== STATUS-WISE REPORT ==========")

    if len(records) == 0:

        print("No complaint data available.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Status          :", row[0])
            print("Complaint Count :", row[1])

    cursor.close()


# ==========================================================
# RECURRING PROBLEMS
# ==========================================================

def recurring_problems(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            location,
            issue,
            COUNT(*) AS occurrences
        FROM complaints
        GROUP BY location, issue
        HAVING COUNT(*) > 1
        ORDER BY occurrences DESC
    """)

    records = cursor.fetchall()

    print("\n========== RECURRING PROBLEMS ==========")

    if len(records) == 0:

        print("No recurring problems found.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Location    :", row[0])
            print("Issue       :", row[1])
            print("Occurrences :", row[2])

    cursor.close()


# ==========================================================
# OPEN COMPLAINTS REPORT
# ==========================================================

def open_complaints_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            complaint_id,
            location,
            issue,
            description,
            department
        FROM complaints
        WHERE LOWER(status) = 'open'
        ORDER BY complaint_id
    """)

    records = cursor.fetchall()

    print("\n========== OPEN COMPLAINTS ==========")

    if len(records) == 0:

        print("No open complaints found.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Complaint ID :", row[0])
            print("Location     :", row[1])
            print("Issue        :", row[2])
            print("Description  :", row[3])
            print("Department   :", row[4])

    cursor.close()


# ==========================================================
# HIGH PRIORITY LOCATIONS
# ==========================================================

def high_priority_report(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            location,
            COUNT(*) AS complaint_count
        FROM complaints
        GROUP BY location
        HAVING COUNT(*) >= 16
        ORDER BY complaint_count DESC
    """)

    records = cursor.fetchall()

    print("\n========== HIGH PRIORITY LOCATIONS ==========")

    if len(records) == 0:

        print("No high-priority locations found.")

    else:

        for row in records:

            print("------------------------------------------")
            print("Location        :", row[0])
            print("Complaint Count :", row[1])
            print("Priority        : HIGH")

    cursor.close()


# ==========================================================
# COMPLETE INFRASTRUCTURE REPORT
# ==========================================================

def complete_report(conn):

    print("\n")
    print("================================================")
    print("       COMMUNITY INFRASTRUCTURE REPORT")
    print("================================================")

    # Total complaints

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM complaints"
    )

    total = cursor.fetchone()[0]

    print("\nTotal Complaints:", total)

    cursor.close()

    # Reports

    location_report(conn)

    issue_report(conn)

    department_report(conn)

    status_report(conn)

    recurring_problems(conn)

    open_complaints_report(conn)

    high_priority_report(conn)

    print("\n================================================")
    print("              REPORT COMPLETED")
    print("================================================")


# ==========================================================
# MAIN MENU
# ==========================================================

def main():

    conn = connect_database()

    if conn is None:

        return

    while True:

        print("\n")
        print("================================================")
        print("     COMMUNITY INFRASTRUCTURE PROBLEM ANALYZER")
        print("================================================")

        print("\n1. Add Complaint")
        print("2. Display All Complaints")
        print("3. Location-wise Report")
        print("4. Issue-wise Report")
        print("5. Department-wise Report")
        print("6. Status-wise Report")
        print("7. Find Recurring Problems")
        print("8. Open Complaints")
        print("9. High Priority Locations")
        print("10. Generate Complete Report")
        print("11. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            add_complaint(conn)

        elif choice == "2":

            display_complaints(conn)

        elif choice == "3":

            location_report(conn)

        elif choice == "4":

            issue_report(conn)

        elif choice == "5":

            department_report(conn)

        elif choice == "6":

            status_report(conn)

        elif choice == "7":

            recurring_problems(conn)

        elif choice == "8":

            open_complaints_report(conn)

        elif choice == "9":

            high_priority_report(conn)

        elif choice == "10":

            complete_report(conn)

        elif choice == "11":

            print("\nThank you for using")
            print("Community Infrastructure Problem Analyzer!")

            break

        else:

            print("\nInvalid choice!")
            print("Please enter a valid option.")

    conn.close()


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    main()
