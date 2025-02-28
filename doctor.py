import tkinter as tk
from tkinter import messagebox
from database import check_user_credentials, get_user_role, conn, retrieve_phr_from_db, check_access
from data_transmission import receive_phr_data

class DoctorInterface:
    def __init__(self, root, main_menu_callback):
        self.root = root
        self.main_menu_callback = main_menu_callback
        self.current_user = None
        self.create_doctor_interface()

    def create_doctor_interface(self):
        self.clear_window()
        tk.Label(self.root, text="Doctor Interface", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="User ID:").pack()
        self.user_id = tk.Entry(self.root)
        self.user_id.pack()
        tk.Label(self.root, text="Password:").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.handle_doctor_login).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu_callback).pack(pady=5)

    def handle_doctor_login(self):
        user_id = self.user_id.get()
        password = self.password.get()
        if check_user_credentials(user_id, password):
            role = get_user_role(user_id)
            if role == "Doctor":
                self.current_user = user_id
                messagebox.showinfo("Success", "Doctor logged in successfully!")
                self.show_doctor_phr_operations()
            else:
                messagebox.showerror("Error", "Access denied. You are not a doctor.")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_doctor_phr_operations(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome, Doctor", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View User List", command=self.view_user_list).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def view_user_list(self):
        self.clear_window()
        tk.Label(self.root, text="User List", font=("Arial", 14)).pack(pady=10)
        users = self.get_user_list()
        for user in users:
            tk.Label(self.root, text=user).pack(pady=5)
            if check_access(user, self.current_user):
                tk.Button(self.root, text="Access PHR File", command=lambda u=user: self.access_phr_file(u)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_doctor_phr_operations).pack(pady=5)

    def access_phr_file(self, patient_id):
        result = retrieve_phr_from_db(patient_id)
        if result:
            encrypted_data, nonce, tag, encrypted_aes_key = result
            if encrypted_data and encrypted_aes_key:
                decrypted_data = receive_phr_data(encrypted_data, encrypted_aes_key, nonce)
                if decrypted_data:
                    try:
                        # Attempt to display as text
                        messagebox.showinfo("PHR Data", decrypted_data)
                    except Exception as e:
                        # If any error occurs, treat it as binary data
                        messagebox.showinfo("PHR Data (Binary)", f"Binary data: {decrypted_data.hex()}")
                else:
                    messagebox.showinfo("Info", "Failed to decrypt PHR data.")
            else:
                messagebox.showinfo("Info", "Incomplete data found.")
        else:
            messagebox.showinfo("Info", "No PHR data found or access not granted.")

    def logout(self):
        self.current_user = None
        self.create_doctor_interface()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_user_list(self):
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE role != 'Doctor'")
        return [row[0] for row in cursor.fetchall()]