# xor_cipher.py

def xor_encrypt(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def xor_decrypt(ciphertext, key):
    return xor_encrypt(ciphertext, key)  # XOR is symmetric

# Example usage
plaintext = "Hello XOR!"
key = "key"
ciphertext = xor_encrypt(plaintext, key)
print("Encrypted (raw):", ciphertext.encode())  # show raw bytes
print("Decrypted:", xor_decrypt(ciphertext, key))
# xor_cipher.py

def xor_encrypt(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def xor_decrypt(ciphertext, key):
    return xor_encrypt(ciphertext, key)  # XOR is symmetric

# Example usage
plaintext = "Hello XOR!"
key = "key"
ciphertext = xor_encrypt(plaintext, key)
print("Encrypted (raw):", ciphertext.encode())  # show raw bytes
print("Decrypted:", xor_decrypt(ciphertext, key))
