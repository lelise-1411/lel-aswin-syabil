def assign_triage_room():
    # --- Validate severity number (must be a whole number from 1-10) ---
    while True:
        severity_input = input("Enter severity number (1-10): ").strip()
        try:
            severity = int(severity_input)
            # Reject non-whole numbers like "5.5" that int() might mishandle
            if float(severity_input) != severity:
                print("Invalid input. Severity must be a whole number.")
                continue
            if severity < 1 or severity > 10:
                print("Invalid input. Severity must be between 1 and 10.")
                continue
            break
        except ValueError:
            print("Invalid input. Severity must be a whole number.")

    # --- Classify room based on severity ---
    if 1 <= severity <= 4:
        room = "Waiting Room"
    elif 5 <= severity <= 7:
        room = "Room 1"
    else:  # 8-10
        room = "Room 2"

    # --- Display summary ---
    print("\n----- Triage Summary -----")
    print(f"Severity Level : {severity}")
    print(f"Assigned Room  : {room}")
    print("---------------------------")

    return room


# Run the program
if __name__ == "__main__":
    assign_triage_room()