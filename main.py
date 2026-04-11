import json

# -------- GLOBAL DATA --------
medicine_stock = {}
patients = {}
doctor_data = {}
appointments = []
revenue = 0
patient_id_counter = 1

# -------- FILE HANDLING --------
def save_data():
    data = {
        "patients": patients,
        "doctor_data": doctor_data,
        "medicine_stock": medicine_stock,
        "appointments": appointments,
        "revenue": revenue,
        "patient_id_counter": patient_id_counter
    }
    with open("hospital_data.json", "w") as f:
        json.dump(data, f)
    print("Data saved!")

def load_data():
    global patients, doctor_data, medicine_stock, appointments, revenue, patient_id_counter
    try:
        with open("hospital_data.json", "r") as f:
            data = json.load(f)
            patients = data["patients"]
            doctor_data = data["doctor_data"]
            medicine_stock = data["medicine_stock"]
            appointments = data["appointments"]
            revenue = data["revenue"]
            patient_id_counter = data["patient_id_counter"]
        print("Data loaded!")
    except:
        print("No previous data found")

# -------- MEDICINE --------
def add_medicine():
    # Store name as lowercase to keep the database consistent
    name = input("Enter medicine name: ").strip().lower()
    qty = int(input("Enter quantity: "))
    medicine_stock[name] = medicine_stock.get(name, 0) + qty
    print(f"Medicine '{name}' added/updated!")

def view_medicine():
    print("\nMedicine Stock:")
    for name, qty in medicine_stock.items():
        # Display as Title Case for professional look
        print(f"{name.capitalize()} : {qty}")
        if qty <= 5:
            print("⚠️ Low stock!")

def use_medicine():
    global revenue
    # Convert input to lower to match stored keys
    name = input("Enter medicine name: ").strip().lower()

    if name in medicine_stock:
        if medicine_stock[name] > 0:
            medicine_stock[name] -= 1
            revenue += 20
            print(f"One {name} used.")
            if medicine_stock[name] <= 5:
                print("⚠️ Low stock alert!")
        else:
            print("Out of stock!")
    else:
        print("Medicine not found")

# -------- PATIENT --------
def add_patient():
    global revenue, patient_id_counter
    name = input("Enter patient name: ").strip()
    doctor = input("Enter doctor name: ").strip()
    fee = int(input("Enter fee: "))

    pid = "P" + str(patient_id_counter)
    patient_id_counter += 1

    patients[pid] = {
        "name": name,
        "doctor": doctor,
        "fee": fee,
        "history": []
    }
    revenue += fee

    if doctor in doctor_data:
        doctor_data[doctor]["patients"] += 1
    else:
        doctor_data[doctor] = {"patients": 1, "appointments": []}

    print("Patient added with ID:", pid)

def search_patient():
    # User can type ID (P1) or name (John) in any case
    search_term = input("Enter patient ID or Name: ").strip().lower()
    found = False

    for pid, p in patients.items():
        # Compare both ID and Name in lowercase
        if pid.lower() == search_term or p["name"].lower() == search_term:
            print("\n--- Patient Details ---")
            print("ID:", pid)
            print("Name:", p["name"])
            print("Doctor:", p["doctor"])
            print("Fee:", p["fee"])
            print("History:", p["history"])
            found = True
    
    if not found:
        print("Patient not found")

def delete_patient():
    global appointments
    # Normalize ID input to uppercase since IDs are stored as 'P1'
    pid = input("Enter patient ID to delete: ").strip().upper()

    if pid in patients:
        doctor = patients[pid]["doctor"]
        if doctor in doctor_data:
            doctor_data[doctor]["patients"] -= 1
        appointments = [a for a in appointments if a["patient_id"] != pid]
        del patients[pid]
        print("Patient deleted")
    else:
        print("Patient ID not found (Try including the 'P')")

def update_patient():
    pid = input("Enter patient ID to update: ").strip().upper()

    if pid in patients:
        p = patients[pid]
        print("Leave blank to keep old value")
        new_name = input("New name: ").strip()
        new_doctor = input("New doctor: ").strip()
        new_fee = input("New fee: ").strip()

        old_doctor = p["doctor"]
        if new_name: p["name"] = new_name
        if new_fee: p["fee"] = int(new_fee)
        if new_doctor:
            p["doctor"] = new_doctor
            doctor_data[old_doctor]["patients"] -= 1
            if new_doctor in doctor_data:
                doctor_data[new_doctor]["patients"] += 1
            else:
                doctor_data[new_doctor] = {"patients": 1, "appointments": []}
        print("Patient updated")
    else:
        print("Patient not found")

# -------- HISTORY --------
def add_history():
    pid = input("Enter patient ID: ").strip().upper()
    if pid in patients:
        record = input("Enter diagnosis/treatment: ")
        patients[pid]["history"].append(record)
        print("History added")
    else:
        print("Patient not found")

def view_history():
    pid = input("Enter patient ID: ").strip().upper()
    if pid in patients:
        print(f"\nHistory for {patients[pid]['name']}:")
        for h in patients[pid]["history"]:
            print("-", h)
    else:
        print("Patient not found")

# -------- APPOINTMENTS --------
def schedule_appointment():
    pid = input("Enter patient ID: ").strip().upper()
    if pid not in patients:
        print("Invalid patient ID")
        return

    doctor = patients[pid]["doctor"]
    time = input("Enter time: ")
    appointment = {"patient_id": pid, "time": time}
    appointments.append(appointment)

    if doctor not in doctor_data:
        doctor_data[doctor] = {"patients": 0, "appointments": []}
    doctor_data[doctor]["appointments"].append(appointment)
    print("Appointment scheduled")

def view_appointments():
    print("\nAppointments:")
    for app in appointments:
        pid = app["patient_id"]
        name = patients[pid]["name"]
        doctor = patients[pid]["doctor"]
        print(f"{app['time']} - {name} (ID: {pid}) with {doctor}")

# -------- DASHBOARD --------
def dashboard():
    print("\n--- DASHBOARD ---")
    print("Total Patients:", len(patients))
    print("Total Revenue:", revenue)
    print("\nDoctor Performance:")
    for doc, data in doctor_data.items():
        print(f"{doc} - Patients: {data['patients']} | Appointments: {len(data['appointments'])}")

# -------- MAIN PROGRAM --------
load_data()

while True:
    # Vertical line formatting for a cleaner menu
    print("\n" + "="*45)
    print(f"{'HOSPITAL MANAGEMENT SYSTEM':^45}")
    print("="*45)
    print(f"{'1. Add Medicine':<22} | {'2. View Medicine':<22}")
    print(f"{'3. Use Medicine':<22} | {'4. Add Patient':<22}")
    print(f"{'5. Search Patient':<22} | {'6. Delete Patient':<22}")
    print(f"{'7. Update Patient':<22} | {'8. Add History':<22}")
    print(f"{'9. View History':<22} | {'10. Schedule Appt':<22}")
    print(f"{'11. View Appts':<22} | {'12. Dashboard':<22}")
    print("-" * 45)
    print(f"{'13. Save & Exit':^45}")
    print("-" * 45)

    choice = input("Enter choice: ").strip()

    if choice == '1':
        add_medicine()
    elif choice == '2':
        view_medicine()
    elif choice == '3':
        use_medicine()
    elif choice == '4':
        add_patient()
    elif choice == '5':
        search_patient()
    elif choice == '6':
        delete_patient()
    elif choice == '7':
        update_patient()
    elif choice == '8':
        add_history()
    elif choice == '9':
        view_history()
    elif choice == '10':
        schedule_appointment()
    elif choice == '11':
        view_appointments()
    elif choice == '12':
        dashboard()
    elif choice == '13':
        save_data()
        print("Exiting system. Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")
