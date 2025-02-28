import os

class AES:
    def __init__(self, key):
        self.key = key
        self.block_size = 16  # AES block size is 128 bits (16 bytes)

    def pad(self, data):
        padding = self.block_size - (len(data) % self.block_size)
        return data + bytes([padding] * padding)

    def unpad(self, data):
        padding = data[-1]
        return data[:-padding]

    def encrypt_block(self, block, key):
        # Simplified block encryption (this is not a real AES implementation)
        return bytes([b ^ k for b, k in zip(block, key)])

    def decrypt_block(self, block, key):
        # Simplified block decryption (this is not a real AES implementation)
        return bytes([b ^ k for b, k in zip(block, key)])

    def encrypt(self, data):
        padded_data = self.pad(data)
        encrypted_data = bytearray()
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            encrypted_block = self.encrypt_block(block, self.key)
            encrypted_data.extend(encrypted_block)
        return bytes(encrypted_data)

    def decrypt(self, encrypted_data):
        decrypted_data = bytearray()
        for i in range(0, len(encrypted_data), self.block_size):
            block = encrypted_data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block, self.key)
            decrypted_data.extend(decrypted_block)
        return self.unpad(decrypted_data)

def encrypt_and_store_phr(user_id, data):
    key = os.urandom(32)  # 256-bit key
    aes = AES(key)
    encrypted_data = aes.encrypt(data)
    nonce = os.urandom(12)  # 96-bit nonce for GCM mode
    tag = os.urandom(16)  # 128-bit tag for GCM mode
    return encrypted_data, nonce, tag, key

def decrypt_phr(encrypted_data, key):
    aes = AES(key)
    decrypted_data = aes.decrypt(encrypted_data)
    return decrypted_data