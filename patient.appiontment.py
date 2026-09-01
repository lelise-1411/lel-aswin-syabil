from datetime import datetime, date, timedelta


def check_appointment_details():
    while True:
        department = input("Enter department (GP/Specialist): ")
        appointment_date = input("Enter appointment date (DD/MM/YYYY): ")

        # Check department
        department_valid = department in ["GP", "Specialist"]

        # Check date
        try:
            entered_date = datetime.strptime(
                appointment_date, "%d/%m/%Y"
            ).date()

            current_date = date.today()
            maximum_date = current_date + timedelta(days=7)

            date_valid = current_date <= entered_date <= maximum_date

        except ValueError:
            date_valid = False
            entered_date = None

        # Display errors
        if not department_valid:
            print("Error: Please enter GP or Specialist")

        if not date_valid:
            print("Error: Date must be correctly entered and within 7 days from today")

        # If everything is valid
        if department_valid and date_valid:
            return department, appointment_date


# Main program
department, appointment_date = check_appointment_details()

print("\nDepartment:", department)
print("Date:", appointment_date)
print("Your appointment is confirmed")