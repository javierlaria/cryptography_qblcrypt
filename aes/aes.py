# WARNING: This script is for educational purposes only. Unauthorized use is illegal and unethical.

from itertools import product
from Crypto.Cipher import AES
import base64

# Safeguard: Limited charset to lowercase letters and digits
CHARSET = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Test ciphertext (AES-256 encrypted message)
# Example: The message "hello world" encrypted with key "abc123"
TEST_CIPHERTEXT = b'gAAAAABfXw+e8JhDzTcZrFQjy5KZlPQ=='

def decrypt_aes_256(ciphertext, key):
    # Pad key to 32 bytes for AES-256
    key = key.ljust(32)[:32].encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX, nonce=b'')
    try:
        decrypted = cipher.decrypt_and_verify(ciphertext, b'')
        return decrypted.decode('utf-8')
    except (ValueError, KeyError):
        return None

def brute_force_decrypt(ciphertext):
    for password in product(CHARSET, repeat=3):
        password_str = ''.join(password)
        decrypted_message = decrypt_aes_256(ciphertext, password_str)
        if decrypted_message:
            print(f"Decrypted message found with key '{password_str}': {decrypted_message}")
            return
    print("No valid key found.")

# Decode base64 encoded ciphertext
decoded_ciphertext = base64.b64decode(TEST_CIPHERTEXT)

# Perform brute-force decryption
brute_force_decrypt(decoded_ciphertext)
