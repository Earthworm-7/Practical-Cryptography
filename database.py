import sqlite3

conn = sqlite3.connect("phr_system.db")

def initialize_database():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phr (
            user_id TEXT PRIMARY KEY,
            encrypted_data BLOB,
            nonce BLOB,
            tag BLOB,
            encrypted_aes_key BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_permissions (
            patient_id TEXT,
            doctor_id TEXT,
            PRIMARY KEY (patient_id, doctor_id)
        )
    """)
    doctors = [
        {"user_id": "doctor123", "password": "password123", "role": "Doctor"},
        {"user_id": "doctor456", "password": "password456", "role": "Doctor"},
        {"user_id": "doctor789", "password": "password789", "role": "Doctor"}
    ]
    for doctor in doctors:
        try:
            cursor.execute("INSERT INTO users (user_id, password, role) VALUES (?, ?, ?)", 
                           (doctor["user_id"], doctor["password"], doctor["role"]))
        except sqlite3.IntegrityError:
            pass
    conn.commit()

def save_user_to_db(user_id, password, role):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, password, role) VALUES (?, ?, ?)", (user_id, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user_credentials(user_id, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result and result[0] == password

def get_user_role(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def save_phr_to_db(user_id, encrypted_data, nonce, tag, encrypted_aes_key):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO phr (user_id, encrypted_data, nonce, tag, encrypted_aes_key)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, encrypted_data, nonce, tag, encrypted_aes_key))
    conn.commit()

def retrieve_phr_from_db(user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT encrypted_data, nonce, tag, encrypted_aes_key FROM phr WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    if result:
        encrypted_data, nonce, tag, encrypted_aes_key = result
        return encrypted_data, nonce, tag, encrypted_aes_key
    return None, None, None, None

def grant_access(patient_id, doctor_id):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO access_permissions (patient_id, doctor_id) VALUES (?, ?)", (patient_id, doctor_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_access(patient_id, doctor_id):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM access_permissions WHERE patient_id = ? AND doctor_id = ?", (patient_id, doctor_id))
    return cursor.fetchone() is not None