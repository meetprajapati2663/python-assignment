import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import datetime

# ================= DATABASE =================
conn = sqlite3.connect("repairmate.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS repairs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    device TEXT,
    issue TEXT,
    status TEXT,
    cost REAL
)
""")

conn.commit()


# ================= OOP =================
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def save(self):
        cursor.execute(
            "INSERT INTO customers(name, phone) VALUES (?,?)",
            (self.name, self.phone)
        )
        conn.commit()


class Repair(Customer):
    def __init__(self, name, phone, device, issue, status, cost):
        super().__init__(name, phone)
        self.device = device
        self.issue = issue
        self.status = status
        self.cost = cost

    def save_repair(self):
        cursor.execute(
            "INSERT INTO repairs(customer, device, issue, status, cost) VALUES (?,?,?,?,?)",
            (self.name, self.device, self.issue, self.status, self.cost)
        )
        conn.commit()


# ================= FILE INVOICE =================
def save_invoice(customer, device, cost):
    try:
        tax = cost * 0.18
        total = cost + tax

        with open("invoice.txt", "a") as f:
            f.write("\n----- Invoice -----\n")
            f.write(f"Date: {datetime.datetime.now()}\n")
            f.write(f"Customer: {customer}\n")
            f.write(f"Device: {device}\n")
            f.write(f"Cost: {cost}\n")
            f.write(f"Tax: {tax}\n")
            f.write(f"Total: {total}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= FUNCTIONS =================
def add_customer():
    try:
        name = name_entry.get()
        phone = phone_entry.get()

        if name == "" or phone == "":
            raise Exception("Fill all fields")

        c = Customer(name, phone)
        c.save()

        messagebox.showinfo("Success", "Customer Added")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_repair():
    try:
        name = name_entry.get()
        phone = phone_entry.get()
        device = device_entry.get()
        issue = issue_entry.get()
        status = status_entry.get()
        cost = float(cost_entry.get())

        r = Repair(name, phone, device, issue, status, cost)
        r.save_repair()

        save_invoice(name, device, cost)

        messagebox.showinfo("Success", "Repair Saved + Invoice Created")

    except ValueError:
        messagebox.showerror("Error", "Cost must be number")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def regex_search():
    try:
        pattern = search_entry.get()

        cursor.execute("SELECT * FROM repairs")
        data = cursor.fetchall()

        result = []

        for row in data:
            if re.search(pattern, row[4], re.IGNORECASE):
                result.append(str(row))

        output.delete(0, tk.END)

        for r in result:
            output.insert(tk.END, r)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= GUI =================
root = tk.Tk()
root.title("RepairMate App")
root.geometry("600x600")

tk.Label(root, text="Customer Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Device").pack()
device_entry = tk.Entry(root)
device_entry.pack()

tk.Label(root, text="Issue").pack()
issue_entry = tk.Entry(root)
issue_entry.pack()

tk.Label(root, text="Status (Pending / Done)").pack()
status_entry = tk.Entry(root)
status_entry.pack()

tk.Label(root, text="Cost").pack()
cost_entry = tk.Entry(root)
cost_entry.pack()

tk.Button(root, text="Add Customer", command=add_customer).pack(pady=5)
tk.Button(root, text="Add Repair", command=add_repair).pack(pady=5)

tk.Label(root, text="Regex Search Status").pack()
search_entry = tk.Entry(root)
search_entry.pack()

tk.Button(root, text="Search", command=regex_search).pack()

output = tk.Listbox(root, width=80)
output.pack(pady=10)

root.mainloop()
