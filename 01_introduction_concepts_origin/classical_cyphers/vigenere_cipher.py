# vigenere_cipher.py

def vigenere_encrypt(text, key):
    result = ''
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + offset) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    decrypt_key = ''.join(chr((26 - (ord(k.lower()) - ord('a'))) % 26 + ord('a')) for k in key)
    return vigenere_encrypt(text, decrypt_key)

# Example usage
plaintext = "HELLO CLASS"
key = "KEY"
ciphertext = vigenere_encrypt(plaintext, key)
print("Encrypted:", ciphertext)
print("Decrypted:", vigenere_decrypt(ciphertext, key))
