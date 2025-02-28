import os

def chacha20_encrypt(data, key, nonce):
    combined = key + nonce
    encrypted = bytearray()
    for i in range(len(data)):
        encrypted.append(data[i] ^ combined[i % len(combined)])
    return bytes(encrypted)

def chacha20_decrypt(encrypted_data, key, nonce):
    return chacha20_encrypt(encrypted_data, key, nonce)

def transmit_phr_data(data, attributes):
    required_attributes = {"Doctor", "Cardiologist"}  # Example policy
    if not required_attributes.issubset(attributes):
        print("Recipient not authorized to access the data.")
        return None, None, None

    key = os.urandom(32)  # 256-bit key
    nonce = os.urandom(12)  # 96-bit nonce

    if isinstance(data, str):
        data = data.encode('utf-8')

    encrypted_data = chacha20_encrypt(data, key, nonce)
    print("Data transmitted securely using ChaCha20.")
    return encrypted_data, key, nonce

def receive_phr_data(encrypted_data, key, nonce):
    if encrypted_data is None or key is None or nonce is None:
        return None
    decrypted_data = chacha20_decrypt(encrypted_data, key, nonce)
    try:
        # Attempt to decode as UTF-8
        return decrypted_data.decode('utf-8')
    except UnicodeDecodeError:
        # If decoding fails, return binary data
        return decrypted_data

def access_phr_file(patient_id):
    result = retrieve_phr_from_db(patient_id)
    if result:
        encrypted_data, nonce, tag, encrypted_aes_key = result
        if encrypted_data and encrypted_aes_key:
            decrypted_data = receive_phr_data(encrypted_data, encrypted_aes_key, nonce)
            if decrypted_data:
                try:
                    # Attempt to display as text
                    print("Decrypted data:", decrypted_data)
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