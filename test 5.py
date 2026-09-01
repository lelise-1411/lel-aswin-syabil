"""
CareBridge Hospital Management System
Integrated Program - Part B
"""

from datetime import datetime, date, timedelta

# ------------------ CONSTANTS ------------------
BASE_FEE = 100
LAB_TEST_RATE = 10
DISCOUNT_RATE = 0.70

WAITING_ROOM_MAX = 4
ROOM_1_MAX = 7
ROOM_2_MAX = 10


# ------------------ FUNCTION: REGISTER PATIENT ------------------
def check_patient_details():
    while True:
        name = input("Enter Name: ")
        try:
            age = int(input("Enter Age: "))
            patient_id = int(input("Enter ID: "))
        except ValueError:
            print("Please enter numbers for Age and ID.")
            continue
        if name == "":
            print("Name cannot be blank. Please re-enter your details.")
        elif age <= 0:
            print("Age must be a positive number. Please re-enter your details.")
        elif patient_id <= 0:
            print("ID must be a positive number. Please re-enter your details.")
        else:
            return name, age, patient_id


def register_patient():
    name, age, patient_id = check_patient_details()
    print("\n--- Patient Details ---")
    print("Name:", name)
    print("Age:", age)
    print("ID:", patient_id)
    print("Patient details saved successfully.")


# ------------------ FUNCTION: BOOK APPOINTMENT ------------------
def check_appointment_details():
    while True:
        department = input("Enter department (GP/Specialist): ")
        appointment_date = input("Enter appointment date (DD/MM/YYYY): ")

        department_valid = department in ["GP", "Specialist"]

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

        if not department_valid:
            print("Error: Please enter GP or Specialist")

        if not date_valid:
            print("Error: Date must be correctly entered and within 7 days from today")

        if department_valid and date_valid:
            return department, appointment_date


def book_appointment():
    department, appointment_date = check_appointment_details()
    print("\nDepartment:", department)
    print("Date:", appointment_date)
    print("Your appointment is confirmed")


# ------------------ FUNCTION: CALCULATE BILL ------------------
def calculate_bill():
    while True:
        patient_type = input("Enter patient type (subsidised/private): ").strip().lower()
        if patient_type in ("subsidised", "private"):
            break
        print("Invalid input. Please enter 'subsidised' or 'private'.")

    while True:
        tests_input = input("Enter number of lab tests: ").strip()
        try:
            num_tests = int(tests_input)
            if num_tests < 0:
                print("Number of lab tests cannot be negative.")
                continue
            if float(tests_input) != num_tests:
                print("Invalid input. Number of lab tests must be a whole number.")
                continue
            break
        except ValueError:
            print("Invalid input. Number of lab tests must be a whole number.")

    subtotal = BASE_FEE + (num_tests * LAB_TEST_RATE)

    if patient_type == "subsidised":
        discount = subtotal * (1 - DISCOUNT_RATE)
        total = subtotal - discount
    else:
        discount = 0
        total = subtotal

    print("\n----- Bill Summary -----")
    print(f"Patient type   : {patient_type.capitalize()}")
    print(f"Base fee       : ${BASE_FEE:.2f}")
    print(f"Lab tests      : {num_tests} x ${LAB_TEST_RATE} = ${num_tests * LAB_TEST_RATE:.2f}")
    print(f"Subtotal       : ${subtotal:.2f}")
    print(f"Discount       : ${discount:.2f}")
    print(f"Total bill     : ${total:.2f}")
    print("-------------------------")

    return total


# ------------------ FUNCTION: ASSIGN TRIAGE ROOM ------------------
def assign_triage_room():
    while True:
        severity_input = input("Enter severity number (1-10): ").strip()
        try:
            severity = int(severity_input)
            if float(severity_input) != severity:
                print("Invalid input. Severity must be a whole number.")
                continue
            if severity < 1 or severity > ROOM_2_MAX:
                print("Invalid input. Severity must be between 1 and 10.")
                continue
            break
        except ValueError:
            print("Invalid input. Severity must be a whole number.")

    if severity <= WAITING_ROOM_MAX:
        room = "Waiting Room"
    elif severity <= ROOM_1_MAX:
        room = "Room 1"
    else:
        room = "Room 2"

    print("\n----- Triage Summary -----")
    print(f"Severity Level : {severity}")
    print(f"Assigned Room  : {room}")
    print("---------------------------")

    return room


# ------------------ MAIN MENU ------------------
def main():
    while True:
        print("\n===== CAREBRIDGE HOSPITAL MENU =====")
        print("1. Register Patient")
        print("2. Book Appointment")
        print("3. Calculate Bill")
        print("4. Assign Triage Room")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_patient()
        elif choice == "2":
            book_appointment()
        elif choice == "3":
            calculate_bill()
        elif choice == "4":
            assign_triage_room()
        elif choice == "5":
            print("Thank you. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()