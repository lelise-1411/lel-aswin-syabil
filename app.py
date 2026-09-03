from flask import Flask, request, render_template_string
from datetime import datetime, date, timedelta

app = Flask(__name__)

# ------------------ CONSTANTS ------------------
BASE_FEE = 100
LAB_TEST_RATE = 10
DISCOUNT_RATE = 0.70

WAITING_ROOM_MAX = 4
ROOM_1_MAX = 7
ROOM_2_MAX = 10

# ------------------ FRONTEND: HTML INTERFACE STRING ------------------
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CareBridge Hospital Management System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; color: #333; display: flex; min-height: 100vh; }
        
        /* Dashboard Layout Structure */
        .sidebar { width: 260px; background-color: #2c3e50; color: white; padding: 20px 0; display: flex; flex-direction: column; box-shadow: 2px 0 10px rgba(0,0,0,0.1); }
        .sidebar-brand { font-size: 1.4rem; font-weight: bold; padding: 0 20px 20px 20px; border-bottom: 1px solid #34495e; margin-bottom: 20px; color: #3498db; }
        .sidebar-menu { list-style: none; padding: 0; margin: 0; }
        .sidebar-item a { display: block; padding: 12px 20px; color: #ecf0f1; text-decoration: none; font-weight: 500; border-left: 4px solid transparent; transition: all 0.2s; }
        .sidebar-item a:hover { background-color: #34495e; border-left-color: #3498db; color: white; }
        .sidebar-item.active a { background-color: #1a252f; border-left-color: #2ecc71; color: white; }
        
        .main-content { flex: 1; padding: 40px; box-sizing: border-box; background-color: #f8fafc; }
        .container { max-width: 800px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0; }
        h2 { color: #34495e; font-size: 1.2rem; margin-top: 10px; margin-bottom: 20px; }
        
        .card { background: #ffffff; border: none; padding: 10px 0; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 0.9rem; }
        input, select { width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #cbd5e1; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #3498db; color: white; border: none; padding: 12px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; font-size: 1rem; }
        button:hover { background-color: #2980b9; }
        
        .alert { padding: 15px; border-radius: 4px; margin-bottom: 20px; font-weight: bold; }
        .error { background-color: #fde8e8; color: #9b1c1c; border-left: 5px solid #e11d48; }
        .success { background-color: #edf7ed; color: #1e4620; border-left: 5px solid #4caf50; }
    </style>
</head>
<body>

<!-- Left Navigation Menu Module -->
<nav class="sidebar">
    <div class="sidebar-brand">🏥 CareBridge Portal</div>
    <ul class="sidebar-menu">
        <li class="sidebar-item {% if active_view == 'register' %}active{% endif %}"><a href="/?view=register">1. Register Patient</a></li>
        <li class="sidebar-item {% if active_view == 'book' %}active{% endif %}"><a href="/?view=book">2. Book Appointment</a></li>
        <li class="sidebar-item {% if active_view == 'bill' %}active{% endif %}"><a href="/?view=bill">3. Calculate Bill</a></li>
        <li class="sidebar-item {% if active_view == 'triage' %}active{% endif %}"><a href="/?view=triage">4. Assign Triage Room</a></li>
    </ul>
</nav>

<!-- Right Main Module Window -->
<main class="main-content">
    <div class="container">
        <h1>CareBridge Hospital Portal</h1>
        
        <!-- Alerts Block -->
        {% if error %}
            <div class="alert error">❌ Error: {{ error }}</div>
        {% endif %}

        {% if result %}
            <div class="alert success">
                <h3>🎉 Action Complete ({{ (action or '').upper() }})</h3>
                {% if action == 'register' %}
                    <p><strong>Patient Registered:</strong> {{ result.name }} (Age: {{ result.age }}, ID: {{ result.id }})</p>
                {% elif action == 'book' %}
                    <p><strong>Appointment Confirmed:</strong> {{ result.department }} Department on {{ result.date }}</p>
                {% elif action == 'bill' %}
                    <p><strong>Billing Calculation Complete:</strong></p>
                    <ul>
                        <li>Type: {{ result.type }}</li>
                        <li>Base Fee: ${{ result.base_fee }}</li>
                        <li>Lab Charges: ${{ result.lab_tests }}</li>
                        <li>Subtotal: ${{ result.subtotal }}</li>
                        <li>Subsidies: -${{ result.discount }}</li>
                        <li><strong>Total Bill: ${{ result.total }}</strong></li>
                    </ul>
                {% elif action == 'triage' %}
                    <p><strong>Triage System Routing:</strong> Severity Level {{ result.severity }} mapped to <strong>👉 {{ result.room }}</strong></p>
                {% endif %}
            </div>
        {% endif %}

        <!-- Dynamic Context Content Panels Matrix -->
        {% if active_view == 'register' %}
        <div class="card">
            <h2>1. Register Patient</h2>
            <form method="POST">
                <input type="hidden" name="action" value="register">
                <label>Full Name</label>
                <input type="text" name="name" required placeholder="e.g. John Doe">
                <label>Age</label>
                <input type="number" name="age" required min="1" placeholder="e.g. 35">
                <label>Patient ID</label>
                <input type="number" name="id" required min="1" placeholder="e.g. 1043">
                <button type="submit">Submit Registration</button>
            </form>
        </div>
        {% elif active_view == 'book' %}
        <div class="card">
            <h2>2. Book Appointment</h2>
            <form method="POST">
                <input type="hidden" name="action" value="book">
                <label>Department</label>
                <select name="department">
                    <option value="GP">General Practitioner (GP)</option>
                    <option value="Specialist">Specialist</option>
                </select>
                <label>Appointment Date (Next 7 Days Only)</label>
                <input type="date" name="date" required>
                <button type="submit">Confirm Date</button>
            </form>
        </div>
        {% elif active_view == 'bill' %}
        <div class="card">
            <h2>3. Calculate Bill</h2>
            <form method="POST">
                <input type="hidden" name="action" value="bill">
                <label>Patient Category</label>
                <select name="type">
                    <option value="subsidised">Subsidised (70% Off)</option>
                    <option value="private">Private</option>
                </select>
                <label>Number of Lab Tests</label>
                <input type="number" name="tests" required min="0" value="0">
                <button type="submit">Run Computations</button>
            </form>
        </div>
        {% elif active_view == 'triage' %}
        <div class="card">
            <h2>4. Assign Triage Room</h2>
            <form method="POST">
                <input type="hidden" name="action" value="triage">
                <label>Severity Level Scale (1 - 10)</label>
                <input type="number" name="severity" required min="1" max="10" placeholder="1=Mild, 10=Critical">
                <button type="submit">Determine Placement</button>
            </form>
        </div>
        {% endif %}
    </div>
</main>

</body>
</html>
"""

# ------------------ BACKEND: ROUTE HANDLING ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # Detect navigation changes using URL parameter filtering (Defaults to 'register')
    active_view = request.args.get("view", "register")
    action = request.form.get("action")
    result = {}
    error = None

    if request.method == "POST":
        if action:
            # Keep the menu view locked on the component tab where the form data was sent
            active_view = action
        
        if action == "register":
            name = request.form.get("name", "").strip()
            age_str = request.form.get("age", "")
            id_str = request.form.get("id", "")
            
            if not name:
                error = "Name cannot be blank."
            else:
                try:
                    age = int(age_str)
                    patient_id = int(id_str)
                    if age <= 0 or patient_id <= 0:
                        error = "Age and ID must be positive numbers."
                    else:
                        result = {"name": name, "age": age, "id": patient_id}
                except ValueError:
                    error = "Age and ID must be whole numbers."

        elif action == "book":
            department = request.form.get("department")
            appointment_date = request.form.get("date", "").strip()

            if department not in ["GP", "Specialist"]:
                error = "Please select a valid department."
            else:
                try:
                    entered_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                    current_date = date.today()
                    maximum_date = current_date + timedelta(days=7)
                    
                    if not (current_date <= entered_date <= maximum_date):
                        error = "Date must be between today and 7 days from now."
                    else:
                        result = {"department": department, "date": entered_date.strftime("%d/%m/%Y")}
                except ValueError:
                    error = "Please enter a valid appointment date."

        elif action == "bill":
            patient_type = request.form.get("type")
            tests_str = request.form.get("tests", "")

            if patient_type not in ["subsidised", "private"]:
                error = "Please select a valid patient category."
            else:
                try:
                    tests = int(tests_str)
                    if tests < 0:
                        error = "The number of lab tests cannot be negative."
                    else:
                        lab_tests = tests * LAB_TEST_RATE
                        subtotal = BASE_FEE + lab_tests
                        discount = subtotal * DISCOUNT_RATE if patient_type == "subsidised" else 0
                        total = subtotal - discount
                        result = {
                            "type": patient_type,
                            "base_fee": f"{BASE_FEE:.2f}",
                            "lab_tests": f"{lab_tests:.2f}",
                            "subtotal": f"{subtotal:.2f}",
                            "discount": f"{discount:.2f}",
                            "total": f"{total:.2f}",
                        }
                except ValueError:
                    error = "The number of lab tests must be a whole number."

        elif action == "triage":
            severity_str = request.form.get("severity", "")

            try:
                severity = int(severity_str)
                if not 1 <= severity <= 10:
                    error = "Severity must be between 1 and 10."
                elif severity <= 3:
                    room = "Waiting Room"
                elif severity <= 6:
                    room = "Room 1"
                else:
                    room = "Room 2"

                if not error:
                    result = {"severity": severity, "room": room}
            except ValueError:
                error = "Severity must be a whole number between 1 and 10."

    return render_template_string(
        HTML_LAYOUT,
        active_view=active_view,
        action=action,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)