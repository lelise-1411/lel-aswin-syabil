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


def main():
    while True:
        print("\n===== PATIENT MENU =====")
        print("1. Enter Patient Details")
        print("2. Display Patient Details")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name, age, patient_id = check_patient_details()
            print("Patient details saved successfully.")

        elif choice == "2":
            try:
                print("\n--- Patient Details ---")
                print("Name:", name)
                print("Age:", age)
                print("ID:", patient_id)
            except NameError:
                print("No patient details entered yet.")

        elif choice == "3":
            print("Thank you. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


main()