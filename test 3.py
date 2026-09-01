def calculate_bill():
    # --- Validate patient type ---
    while True:
        patient_type = input("Enter patient type (subsidised/private): ").strip().lower()
        if patient_type in ("subsidised", "private"):
            break
        print("Invalid input. Please enter 'subsidised' or 'private'.")

    # --- Validate number of lab tests (must be a whole number) ---
    while True:
        tests_input = input("Enter number of lab tests: ").strip()
        try:
            num_tests = int(tests_input)
            if num_tests < 0:
                print("Number of lab tests cannot be negative.")
                continue
            # Reject inputs like "3.5" that int() might mis-happily parse via float
            if float(tests_input) != num_tests:
                print("Invalid input. Number of lab tests must be a whole number.")
                continue
            break
        except ValueError:
            print("Invalid input. Number of lab tests must be a whole number.")

    # --- Calculate bill ---
    base_fee = 100
    lab_test_rate = 10
    subtotal = base_fee + (num_tests * lab_test_rate)

    if patient_type == "subsidised":
        discount = subtotal * 0.30
        total = subtotal - discount
    else:
        discount = 0
        total = subtotal

    # --- Display results ---
    print("\n----- Bill Summary -----")
    print(f"Patient type   : {patient_type.capitalize()}")
    print(f"Base fee       : ${base_fee:.2f}")
    print(f"Lab tests      : {num_tests} x ${lab_test_rate} = ${num_tests * lab_test_rate:.2f}")
    print(f"Subtotal       : ${subtotal:.2f}")
    print(f"Discount       : ${discount:.2f}")
    print(f"Total bill     : ${total:.2f}")
    print("-------------------------")

    return total


# Run the program
if __name__ == "__main__":
    calculate_bill()