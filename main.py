medicine_stock = {}
patients = []
revenue = 0
doctor_data = {}

# -------- MEDICINE --------
def add_medicine():
    name = input("Enter medicine name: ")
    qty = int(input("Enter quantity: "))
    medicine_stock[name] = qty
    print("Medicine added!")

def view_medicine():
    print("\nMedicine Stock:")
    for name, qty in medicine_stock.items():
        print(name, ":", qty)
        if qty <= 5:
            print("⚠️ Low stock!")

def use_medicine():
    global revenue
    name = input("Enter medicine name: ")
    
    if name in medicine_stock:
        medicine_stock[name] -= 1
        revenue += 20
        print("Medicine used")
        
        if medicine_stock[name] <= 5:
            print("⚠️ Low stock alert!")
    else:
        print("Medicine not found")

# -------- PATIENT --------
def add_patient():
    global revenue
    name = input("Enter patient name: ")
    doctor = input("Enter doctor name: ")
    fee = int(input("Enter fee: "))
    
    patients.append(name)
    revenue += fee
    
    if doctor in doctor_data:
        doctor_data[doctor] += 1
    else:
        doctor_data[doctor] = 1
    
    print("Patient added!")

# -------- DASHBOARD --------
def dashboard():
    print("\n--- DASHBOARD ---")
    print("Total Patients:", len(patients))
    print("Total Revenue:", revenue)
    
    print("\nDoctor Performance:")
    for doc, count in doctor_data.items():
        print(doc, ":", count)

# -------- MENU --------
while True:
    print("\n1.Add Medicine")
    print("2.View Medicine")
    print("3.Use Medicine")
    print("4.Add Patient")
    print("5.Dashboard")
    print("6.Exit")
    
    choice = input("Enter choice: ")
    
    if choice == '1':
        add_medicine()
    elif choice == '2':
        view_medicine()
    elif choice == '3':
        use_medicine()
    elif choice == '4':
        add_patient()
    elif choice == '5':
        dashboard()
    elif choice == '6':
        break
    else:
        print("Invalid choice")