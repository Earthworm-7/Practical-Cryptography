import tkinter as tk
from tkinter import messagebox, filedialog
from user_auth import register_user, login_user
from database import initialize_database, save_phr_to_db, retrieve_phr_from_db, grant_access
from data_encryption import encrypt_and_store_phr, decrypt_phr
from doctor import DoctorInterface


class PHRSystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Privacy-Preserving PHR System")
        self.root.geometry("600x400")
        self.current_user = None
        self.user_role = None

    def run(self):
        initialize_database()
        self.show_role_selection()
        self.root.mainloop()

    def show_role_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Select Your Role", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Patient", command=self.show_patient_interface).pack(pady=5)
        tk.Button(self.root, text="Doctor", command=self.show_doctor_interface).pack(pady=5)

    def show_patient_interface(self):
        self.user_role = "Patient"
        self.show_main_menu()

    def show_doctor_interface(self):
        self.user_role = "Doctor"
        self.doctor_interface = DoctorInterface(self.root, self.show_role_selection)

    def show_main_menu(self):
        self.clear_window()
        if self.user_role == "Patient":
            tk.Label(self.root, text="--- Patient PHR System ---", font=("Arial", 16)).pack(pady=10)
            tk.Button(self.root, text="Register", command=self.register_user).pack(pady=5)
            tk.Button(self.root, text="Login", command=self.login_user).pack(pady=5)
            tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)
        elif self.user_role == "Doctor":
            self.show_doctor_interface()

    def register_user(self):
        self.clear_window()
        tk.Label(self.root, text="Register New User", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="User ID:").pack()
        user_id = tk.Entry(self.root)
        user_id.pack()
        tk.Label(self.root, text="Password:").pack()
        password = tk.Entry(self.root, show="*")
        password.pack()
        tk.Button(self.root, text="Register", command=lambda: self.handle_registration(user_id.get(), password.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_interface).pack()

    def handle_registration(self, user_id, password):
        role = "Patient"
        if register_user(user_id, password, role):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Registration failed!")
        self.show_patient_interface()

    def login_user(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="User ID:").pack()
        user_id = tk.Entry(self.root)
        user_id.pack()
        tk.Label(self.root, text="Password:").pack()
        password = tk.Entry(self.root, show="*")
        password.pack()
        tk.Button(self.root, text="Login", command=lambda: self.handle_login(user_id.get(), password.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_interface).pack()

    def handle_login(self, user_id, password):
        if login_user(user_id, password):
            self.current_user = user_id
            messagebox.showinfo("Success", "Login successful!")
            self.show_phr_operations()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_phr_operations(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Encrypt and Store PHR", command=self.encrypt_and_store_phr).pack(pady=5)
        tk.Button(self.root, text="Access PHR", command=self.access_phr).pack(pady=5)
        tk.Button(self.root, text="Grant Access", command=self.grant_access_to_doctor).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    
    def access_phr(self):
        encrypted_data, _, _, key = retrieve_phr_from_db(self.current_user)
        if encrypted_data and key:
            decrypted_data = decrypt_phr(encrypted_data, key)
            messagebox.showinfo("PHR Data", decrypted_data.decode('utf-8'))
        else:
            messagebox.showinfo("Info", "No PHR data found.")
    
    def encrypt_and_store_phr(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])
        if not file_path:
            messagebox.showinfo("Info", "No file selected. Operation canceled.")
            return

        with open(file_path, "rb") as file:
            phr_data = file.read()

        # Unpack all four returned values
        encrypted_data, nonce, tag, key = encrypt_and_store_phr(self.current_user, phr_data)
        save_phr_to_db(self.current_user, encrypted_data, nonce, tag, key)
        messagebox.showinfo("Success", "PHR encrypted and stored successfully!")

    def grant_access_to_doctor(self):
        self.clear_window()
        tk.Label(self.root, text="Grant Access to Doctor", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Doctor ID:").pack()
        doctor_id = tk.Entry(self.root)
        doctor_id.pack()
        tk.Button(self.root, text="Grant Access", command=lambda: self.handle_grant_access(doctor_id.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_phr_operations).pack()

    def handle_grant_access(self, doctor_id):
        if grant_access(self.current_user, doctor_id):
            messagebox.showinfo("Success", "Access granted to doctor successfully!")
        else:
            messagebox.showerror("Error", "Failed to grant access.")
        self.show_phr_operations()

    def logout(self):
        self.current_user = None
        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = PHRSystemGUI()
    app.run()