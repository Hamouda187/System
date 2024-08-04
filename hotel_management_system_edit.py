import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            availability TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            number TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            remaining REAL
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute('SELECT * FROM admin WHERE username = "admin"')
    if not cursor.fetchone():
        cursor.execute('INSERT INTO admin (username, password) VALUES ("admin", "123")')
    
    conn.commit()
    conn.close()

# Main application class
class HotelManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("800x600")
        self.username = ""
        self.conn = sqlite3.connect('hotel_management.db')
        init_db()
        self.create_login_page()
        
    def create_login_page(self):
        self.clear_window()
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.exit_button = ttk.Button(self.login_frame, text="Exit", command=self.quit)
        self.exit_button.grid(row=3, column=0, columnspan=2, pady=5)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, password))
        admin = cursor.fetchone()
        
        cursor.execute('SELECT * FROM employee WHERE username=? AND password=?', (username, password))
        employee = cursor.fetchone()
        
        if admin:
            self.username = username
            self.create_admin_page()
        elif employee:
            self.username = username
            self.create_employee_page()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")
        
    def create_admin_page(self):
        self.clear_window()
        self.username_label = ttk.Label(self, text=f"Welcome, {self.username}", anchor='e')
        self.username_label.pack(fill=tk.X, padx=5, pady=5)
        
        self.admin_frame = ttk.Frame(self)
        self.admin_frame.pack(padx=20, pady=20)
        
        ttk.Button(self.admin_frame, text="Add Hotel", command=self.create_add_hotel_page).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Edit Hotel", command=self.create_edit_hotel_page).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Delete Hotel", command=self.create_delete_hotel_page).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Add Employee", command=self.create_add_employee_page).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Remove Employee", command=self.create_remove_employee_page).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="View Hotels", command=self.create_view_hotels_page).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="View Employees", command=self.create_view_employees_page).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Add Reservation", command=self.create_add_reservation_page).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Edit Reservation", command=self.create_edit_reservation_page).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="View Reservations", command=self.create_view_reservations_page).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(self.admin_frame, text="Sign Out", command=self.create_login_page).grid(row=4, column=1, padx=5, pady=5)
        
    def create_employee_page(self):
        self.clear_window()
        self.username_label = ttk.Label(self, text=f"Welcome, {self.username}", anchor='e')
        self.username_label.pack(fill=tk.X, padx=5, pady=5)
        
        self.employee_frame = ttk.Frame(self)
        self.employee_frame.pack(padx=20, pady=20)
        
        ttk.Button(self.employee_frame, text="View Hotels", command=self.create_view_hotels_page).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.employee_frame, text="Add Reservation", command=self.create_add_reservation_page).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.employee_frame, text="Edit Reservation", command=self.create_edit_reservation_page).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.employee_frame, text="View Reservations", command=self.create_view_reservations_page).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.employee_frame, text="Change Password", command=self.create_change_password_page).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.employee_frame, text="Sign Out", command=self.create_login_page).grid(row=5, column=0, padx=5, pady=5)
        
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
            
    def create_add_hotel_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.add_hotel_frame = ttk.Frame(self)
        self.add_hotel_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.add_hotel_frame, text="Hotel Name:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_name_entry = ttk.Entry(self.add_hotel_frame)
        self.hotel_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_hotel_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.hotel_price_entry = ttk.Entry(self.add_hotel_frame)
        self.hotel_price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_hotel_frame, text="Availability:").grid(row=2, column=0, padx=5, pady=5)
        self.hotel_availability_combobox = ttk.Combobox(self.add_hotel_frame, values=["Available", "Not Available"])
        self.hotel_availability_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        self.add_hotel_button = ttk.Button(self.add_hotel_frame, text="Add Hotel", command=self.add_hotel)
        self.add_hotel_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def add_hotel(self):
        name = self.hotel_name_entry.get()
        price = self.hotel_price_entry.get()
        availability = self.hotel_availability_combobox.get()
        
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO hotel (name, price, availability) VALUES (?, ?, ?)', (name, price, availability))
        self.conn.commit()
        messagebox.showinfo("Success", "Hotel added successfully.")
        self.create_admin_page()
        
    def create_edit_hotel_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.edit_hotel_frame = ttk.Frame(self)
        self.edit_hotel_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.edit_hotel_frame, text="Select Hotel:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_combobox = ttk.Combobox(self.edit_hotel_frame)
        self.hotel_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_hotels()
        
        ttk.Label(self.edit_hotel_frame, text="New Name:").grid(row=1, column=0, padx=5, pady=5)
        self.new_hotel_name_entry = ttk.Entry(self.edit_hotel_frame)
        self.new_hotel_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.edit_hotel_frame, text="New Price:").grid(row=2, column=0, padx=5, pady=5)
        self.new_hotel_price_entry = ttk.Entry(self.edit_hotel_frame)
        self.new_hotel_price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.edit_hotel_frame, text="New Availability:").grid(row=3, column=0, padx=5, pady=5)
        self.new_hotel_availability_combobox = ttk.Combobox(self.edit_hotel_frame, values=["Available", "Not Available"])
        self.new_hotel_availability_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        self.edit_hotel_button = ttk.Button(self.edit_hotel_frame, text="Update Hotel", command=self.edit_hotel)
        self.edit_hotel_button.grid(row=4, column=0, columnspan=2, pady=10)
        
    def load_hotels(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM hotel')
        hotels = cursor.fetchall()
        self.hotel_combobox['values'] = [hotel[0] for hotel in hotels]
        
    def edit_hotel(self):
        old_name = self.hotel_combobox.get()
        new_name = self.new_hotel_name_entry.get()
        new_price = self.new_hotel_price_entry.get()
        new_availability = self.new_hotel_availability_combobox.get()
        
        cursor = self.conn.cursor()
        cursor.execute('UPDATE hotel SET name=?, price=?, availability=? WHERE name=?', (new_name, new_price, new_availability, old_name))
        self.conn.commit()
        messagebox.showinfo("Success", "Hotel updated successfully.")
        self.create_admin_page()
        
    def create_delete_hotel_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.delete_hotel_frame = ttk.Frame(self)
        self.delete_hotel_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.delete_hotel_frame, text="Select Hotel to Delete:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_combobox = ttk.Combobox(self.delete_hotel_frame)
        self.hotel_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_hotels()
        
        self.delete_hotel_button = ttk.Button(self.delete_hotel_frame, text="Delete Hotel", command=self.delete_hotel)
        self.delete_hotel_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    def delete_hotel(self):
        name = self.hotel_combobox.get()
        
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM hotel WHERE name=?', (name,))
        self.conn.commit()
        messagebox.showinfo("Success", "Hotel deleted successfully.")
        self.create_admin_page()
        
    def create_add_employee_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.add_employee_frame = ttk.Frame(self)
        self.add_employee_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.add_employee_frame, text="Employee Name:").grid(row=0, column=0, padx=5, pady=5)
        self.employee_name_entry = ttk.Entry(self.add_employee_frame)
        self.employee_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_employee_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.employee_password_entry = ttk.Entry(self.add_employee_frame, show="*")
        self.employee_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.add_employee_button = ttk.Button(self.add_employee_frame, text="Add Employee", command=self.add_employee)
        self.add_employee_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def add_employee(self):
        username = self.employee_name_entry.get()
        password = self.employee_password_entry.get()
        
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO employee (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()
        messagebox.showinfo("Success", "Employee added successfully.")
        self.create_admin_page()
        
    def create_remove_employee_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.remove_employee_frame = ttk.Frame(self)
        self.remove_employee_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.remove_employee_frame, text="Select Employee to Remove:").grid(row=0, column=0, padx=5, pady=5)
        self.remove_employee_combobox = ttk.Combobox(self.remove_employee_frame)
        self.remove_employee_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_employees()
        
        self.remove_employee_button = ttk.Button(self.remove_employee_frame, text="Remove Employee", command=self.remove_employee)
        self.remove_employee_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    def load_employees(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, username FROM employee')
        employees = cursor.fetchall()
        employee_names = [f"{employee[1]}" for employee in employees]
        self.remove_employee_combobox['values'] = employee_names
        self.remove_employee_combobox.bind("<<ComboboxSelected>>", self.load_employee_details)
        
    def load_employee_details(self, event):
        selected_name = self.remove_employee_combobox.get()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employee WHERE username=?', (selected_name,))
        employee = cursor.fetchone()
        if employee:
            self.current_employee_id = employee[0]
        
    def remove_employee(self):
        selected_name = self.remove_employee_combobox.get()
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM employee WHERE username=?', (selected_name,))
        self.conn.commit()
        messagebox.showinfo("Success", "Employee removed successfully.")
        self.create_admin_page()
        
    def create_view_hotels_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page if self.username == 'admin' else self.create_employee_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.view_hotels_frame = ttk.Frame(self)
        self.view_hotels_frame.pack(padx=20, pady=20)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM hotel')
        hotels = cursor.fetchall()
        
        self.hotels_tree = ttk.Treeview(self.view_hotels_frame, columns=("ID", "Name", "Price", "Availability"), show='headings')
        self.hotels_tree.heading("ID", text="ID")
        self.hotels_tree.heading("Name", text="Name")
        self.hotels_tree.heading("Price", text="Price")
        self.hotels_tree.heading("Availability", text="Availability")
        
        for hotel in hotels:
            self.hotels_tree.insert("", "end", values=hotel)
            
        self.hotels_tree.pack()
        
    def create_view_employees_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.view_employees_frame = ttk.Frame(self)
        self.view_employees_frame.pack(padx=20, pady=20)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employee')
        employees = cursor.fetchall()
        
        self.employees_tree = ttk.Treeview(self.view_employees_frame, columns=("ID", "Username"), show='headings')
        self.employees_tree.heading("ID", text="ID")
        self.employees_tree.heading("Username", text="Username")
        
        for employee in employees:
            self.employees_tree.insert("", "end", values=employee)
            
        self.employees_tree.pack()
        
    def create_add_reservation_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page if self.username == 'admin' else self.create_employee_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.add_reservation_frame = ttk.Frame(self)
        self.add_reservation_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.add_reservation_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.reservation_name_entry = ttk.Entry(self.add_reservation_frame)
        self.reservation_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_reservation_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.reservation_email_entry = ttk.Entry(self.add_reservation_frame)
        self.reservation_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_reservation_frame, text="Number:").grid(row=2, column=0, padx=5, pady=5)
        self.reservation_number_entry = ttk.Entry(self.add_reservation_frame)
        self.reservation_number_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_reservation_frame, text="Date:").grid(row=3, column=0, padx=5, pady=5)
        self.reservation_date_entry = ttk.Entry(self.add_reservation_frame)
        self.reservation_date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_reservation_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5)
        self.reservation_status_combobox = ttk.Combobox(self.add_reservation_frame, values=["Paid", "Pending", "Paid Part"])
        self.reservation_status_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.reservation_status_combobox.bind("<<ComboboxSelected>>", self.update_remaining_field)
        
        self.remaining_label = ttk.Label(self.add_reservation_frame, text="Remaining:")
        self.remaining_entry = ttk.Entry(self.add_reservation_frame)
        
        self.remaining_label.grid(row=5, column=0, padx=5, pady=5)
        self.remaining_entry.grid(row=5, column=1, padx=5, pady=5)
        
        self.add_reservation_button = ttk.Button(self.add_reservation_frame, text="Add Reservation", command=self.add_reservation)
        self.add_reservation_button.grid(row=6, column=0, columnspan=2, pady=10)
        
    def update_remaining_field(self, event):
        status = self.reservation_status_combobox.get()
        if status == "Paid Part":
            self.remaining_entry.config(state='normal')
        else:
            self.remaining_entry.config(state='disabled')
        
    def add_reservation(self):
        name = self.reservation_name_entry.get()
        email = self.reservation_email_entry.get()
        number = self.reservation_number_entry.get()
        date = self.reservation_date_entry.get()
        status = self.reservation_status_combobox.get()
        remaining = self.remaining_entry.get() if status == "Paid Part" else None
        
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO reservation (name, email, number, date, status, remaining) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, email, number, date, status, remaining))
        self.conn.commit()
        messagebox.showinfo("Success", "Reservation added successfully.")
        self.create_admin_page() if self.username == 'admin' else self.create_employee_page()
        
    def create_edit_reservation_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page if self.username == 'admin' else self.create_employee_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.edit_reservation_frame = ttk.Frame(self)
        self.edit_reservation_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.edit_reservation_frame, text="Select Reservation:").grid(row=0, column=0, padx=5, pady=5)
        self.reservation_combobox = ttk.Combobox(self.edit_reservation_frame)
        self.reservation_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_reservations()
        
        self.edit_reservation_button = ttk.Button(self.edit_reservation_frame, text="Edit Reservation", command=self.edit_reservation)
        self.edit_reservation_button.grid(row=0, column=5, columnspan=2, pady=10)
        
    def load_reservations(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM reservation')
        reservations = cursor.fetchall()
        reservation_names = [f"{reservation[1]}" for reservation in reservations]
        self.reservation_combobox['values'] = reservation_names
        self.reservation_combobox.bind("<<ComboboxSelected>>", self.load_reservation_details)
        
    def load_reservation_details(self, event):
        selected_name = self.reservation_combobox.get()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reservation WHERE name=?', (selected_name,))
        reservation = cursor.fetchone()
        if reservation:
            self.current_reservation_id = reservation[0]
            self.reservation_name_entry = ttk.Entry(self.edit_reservation_frame)
            self.reservation_name_entry.grid(row=1, column=1, padx=5, pady=5)
            self.reservation_name_entry.insert(0, reservation[1])
            
            self.reservation_email_entry = ttk.Entry(self.edit_reservation_frame)
            self.reservation_email_entry.grid(row=2, column=1, padx=5, pady=5)
            self.reservation_email_entry.insert(0, reservation[2])
            
            self.reservation_number_entry = ttk.Entry(self.edit_reservation_frame)
            self.reservation_number_entry.grid(row=3, column=1, padx=5, pady=5)
            self.reservation_number_entry.insert(0, reservation[3])
            
            self.reservation_date_entry = ttk.Entry(self.edit_reservation_frame)
            self.reservation_date_entry.grid(row=4, column=1, padx=5, pady=5)
            self.reservation_date_entry.insert(0, reservation[4])
            
            self.reservation_status_combobox = ttk.Combobox(self.edit_reservation_frame, values=["Paid", "Pending", "Paid Part"])
            self.reservation_status_combobox.grid(row=5, column=1, padx=5, pady=5)
            self.reservation_status_combobox.set(reservation[5])
            self.reservation_status_combobox.bind("<<ComboboxSelected>>", self.update_remaining_field)
            
            self.remaining_label = ttk.Label(self.edit_reservation_frame, text="Remaining:")
            self.remaining_entry = ttk.Entry(self.edit_reservation_frame)
            self.remaining_label.grid(row=6, column=0, padx=5, pady=5)
            self.remaining_entry.grid(row=6, column=1, padx=5, pady=5)
            if reservation[6] is not None:
                self.remaining_entry.insert(0, reservation[6])
                
    def edit_reservation(self):
        name = self.reservation_name_entry.get()
        email = self.reservation_email_entry.get()
        number = self.reservation_number_entry.get()
        date = self.reservation_date_entry.get()
        status = self.reservation_status_combobox.get()
        remaining = self.remaining_entry.get() if status == "Paid Part" else None
        
        cursor = self.conn.cursor()
        cursor.execute('UPDATE reservation SET name=?, email=?, number=?, date=?, status=?, remaining=? WHERE id=?',
                       (name, email, number, date, status, remaining, self.current_reservation_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Reservation updated successfully.")
        self.create_admin_page() if self.username == 'admin' else self.create_employee_page()
        
    def create_view_reservations_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_admin_page if self.username == 'admin' else self.create_employee_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.view_reservations_frame = ttk.Frame(self)
        self.view_reservations_frame.pack(padx=20, pady=20)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reservation')
        reservations = cursor.fetchall()
        
        self.reservations_tree = ttk.Treeview(self.view_reservations_frame, columns=("ID", "Name", "Email", "Number", "Date", "Status", "Remaining"), show='headings')
        self.reservations_tree.heading("ID", text="ID")
        self.reservations_tree.heading("Name", text="Name")
        self.reservations_tree.heading("Email", text="Email")
        self.reservations_tree.heading("Number", text="Number")
        self.reservations_tree.heading("Date", text="Date")
        self.reservations_tree.heading("Status", text="Status")
        self.reservations_tree.heading("Remaining", text="Remaining")
        
        for reservation in reservations:
            self.reservations_tree.insert("", "end", values=reservation)
            
        self.reservations_tree.pack()
        
    def create_change_password_page(self):
        self.clear_window()
        self.back_button = ttk.Button(self, text="Back", command=self.create_employee_page)
        self.back_button.pack(anchor='w', padx=5, pady=5)
        
        self.change_password_frame = ttk.Frame(self)
        self.change_password_frame.pack(padx=20, pady=20)
        
        ttk.Label(self.change_password_frame, text="Current Password:").grid(row=0, column=0, padx=5, pady=5)
        self.current_password_entry = ttk.Entry(self.change_password_frame, show="*")
        self.current_password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.change_password_frame, text="New Password:").grid(row=1, column=0, padx=5, pady=5)
        self.new_password_entry = ttk.Entry(self.change_password_frame, show="*")
        self.new_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.change_password_frame, text="Confirm New Password:").grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password_entry = ttk.Entry(self.change_password_frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.change_password_button = ttk.Button(self.change_password_frame, text="Change Password", command=self.change_password)
        self.change_password_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT password FROM employee WHERE username=?', (self.username,))
        stored_password = cursor.fetchone()[0]
        
        if stored_password != current_password:
            messagebox.showerror("Error", "Current password is incorrect.")
            return
        
        cursor.execute('UPDATE employee SET password=? WHERE username=?', (new_password, self.username))
        self.conn.commit()
        messagebox.showinfo("Success", "Password changed successfully.")
        self.create_employee_page()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = HotelManagementApp()
    app.mainloop()
