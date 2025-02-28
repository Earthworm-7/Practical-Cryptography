from database import retrieve_phr_from_db
from tkinter import messagebox

# Custom XOR-based decryption function
def xor_decrypt(data, key):
    """
    Simple XOR decryption.
    This is not secure for real-world use but serves as a placeholder.
    """
    decrypted = bytearray()
    for i in range(len(data)):
        decrypted.append(data[i] ^ key[i % len(key)])
    return decrypted

# Custom ABE decryption simulation
def abe_decrypt(encrypted_key, attributes):
    """
    Custom ABE decryption simulation.
    In a real implementation, this would use attributes to decrypt the key.
    Here, we assume the key is already decrypted and return it as-is.
    """
    print(f"Decrypting key with attributes: {attributes}")
    return encrypted_key  # Return the key as-is for simulation

def access_phr(user_id):
    result = retrieve_phr_from_db(user_id)
    if result:
        encrypted_data, nonce, tag, encrypted_aes_key = result

        # Decrypt AES key with ABE (simulated)
        attributes = ["Patient"]
        decrypted_aes_key = abe_decrypt(encrypted_aes_key, attributes)

        # Decrypt PHR data using custom XOR decryption
        try:
            decrypted_data = xor_decrypt(encrypted_data, decrypted_aes_key)
            print(f"Decrypted PHR Data: {decrypted_data.decode('utf-8', errors='replace')}")
            messagebox.showinfo("Success", f"Decrypted PHR Data: {decrypted_data.decode('utf-8', errors='replace')}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    else:
        messagebox.showinfo("Info", f"No PHR found for user {user_id}")