# monoalphabetic_cipher.py
import random
import string

def create_substitution_key():
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(text, key):
    result = ''
    for char in text:
        if char.isalpha():
            lower_char = char.lower()
            sub = key[lower_char]
            result += sub.upper() if char.isupper() else sub
        else:
            result += char
    return result

def decrypt(text, key):
    inverse_key = {v: k for k, v in key.items()}
    return encrypt(text, inverse_key)

# Generate a random key once
key = create_substitution_key()
plaintext = "Secret Message Here!"
ciphertext = encrypt(plaintext, key)
decrypted = decrypt(ciphertext, key)

print("Key:", key)
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted)
