# ==========================
# Classic Cipher Interactive Lab for Students
# ==========================
# This program helps you learn about famous historic ciphers.
# You can encrypt, decrypt, brute-force, and experiment!
# Every step is explained with comments.
# ==========================

import string
import random

# ----- CAESAR CIPHER FUNCTIONS -----

def caesar_encrypt(text, shift):
    """Encrypt text using Caesar cipher with a given shift."""
    result = ""
    for char in text:
        if char.isalpha():  # Check if character is a letter (not punctuation or number)
            base = ord('A') if char.isupper() else ord('a')  # Find ASCII base (A or a)
            # Shift character and wrap around alphabet using modulo
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char  # Non-letters are unchanged
    return result

def caesar_decrypt(text, shift):
    """Decrypt text encrypted with Caesar cipher and known shift."""
    return caesar_encrypt(text, -shift)

def caesar_bruteforce(text):
    """Try all possible shifts when shift key is unknown."""
    print("\nBrute-force results for Caesar cipher:")
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        print(f"Shift {shift:2}: {decrypted}")


# ----- VIGENÈRE CIPHER FUNCTIONS -----

def vigenere_encrypt(text, key):
    """Encrypt text using the Vigenère cipher and a keyword."""
    result = ''
    key = key.lower()
    key_index = 0  # Track where we are in the key
    for char in text:
        if char.isalpha():
            # Get shift for this key letter (0 for 'a', ... 25 for 'z')
            offset = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + offset) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    """Decrypt Vigenère cipher with known keyword."""
    result = ''
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            # Get inverse shift for this key letter
            offset = ord('a') - ord(key[key_index % len(key)])
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + offset) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

# ----- MONOALPHABETIC SUBSTITUTION CIPHER -----

def create_mono_key():
    """Create a random substitution key mapping a-z to a permutation of a-z."""
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    # Map 'a'->'x', 'b'->'q', etc.
    return dict(zip(letters, shuffled))

def mono_encrypt(text, key):
    """Encrypt with monoalphabetic (simple) substitution using provided key dict."""
    result = ''
    for char in text:
        if char.isalpha():
            lower = char.lower()
            encoded = key[lower]
            if char.isupper():
                encoded = encoded.upper()
            result += encoded
        else:
            result += char
    return result

def mono_decrypt(text, key):
    """Decrypt monoalphabetic cipher with provided key dict."""
    # Reverse the key mapping
    reverse_key = {v: k for k, v in key.items()}
    return mono_encrypt(text, reverse_key)

def show_mono_key(key):
    """Show the current monoalphabetic key mapping."""
    print("Monoalphabetic Key:")
    print(" ".join(key.keys()))
    print(" ".join(key.values()))

# ----- XOR CIPHER -----

def xor_encrypt(text, key):
    """Encrypt text with XOR cipher given a (short string) key."""
    result = ""
    for i in range(len(text)):
        char = text[i]
        key_char = key[i % len(key)]
        # XOR each char in plaintext with key char, then convert back to character
        result += chr(ord(char) ^ ord(key_char))
    return result

def xor_decrypt(ciphertext, key):
    """Decrypt XOR (same as encryption, because XOR is reversible)."""
    return xor_encrypt(ciphertext, key)  # XOR twice returns original

# ---- MAIN MENU ----

def main():
    print("="*40)
    print(" Welcome to Classic Cipher Interactive Lab ")
    print("="*40)
    mono_key = create_mono_key()  # Pre-generate a monoalphabetic random key
    while True:
        print("\nChoose a cipher or action:")
        print(" 1. Caesar Cipher (Encrypt/Decrypt/Brute-force)")
        print(" 2. Vigenère Cipher (Encrypt/Decrypt)")
        print(" 3. Monoalphabetic Substitution (Encrypt/Decrypt)")
        print(" 4. XOR Cipher (Encrypt/Decrypt)")
        print(" 5. Generate new random Monoalphabetic key")
        print(" 0. Exit\n")
        choice = input("Enter your choice (0-5): ")

        if choice == "1":
            # Caesar Cipher interactive mode
            print("\n--- Caesar Cipher ---")
            text = input("Enter text: ")
            mode = input("Type 'e' to encrypt, 'd' to decrypt, 'b' to brute-force: ").lower()
            if mode == 'e':
                shift = int(input("Enter shift value (0-25): "))
                result = caesar_encrypt(text, shift)
                print("Encrypted:", result)
            elif mode == 'd':
                shift = int(input("Enter shift value used for encryption: "))
                result = caesar_decrypt(text, shift)
                print("Decrypted:", result)
            elif mode == 'b':
                caesar_bruteforce(text)
            else:
                print("Unknown option.")

        elif choice == "2":
            print("\n--- Vigenère Cipher ---")
            text = input("Enter text: ")
            key = input("Enter keyword (letters only, no spaces): ")
            mode = input("Type 'e' to encrypt, 'd' to decrypt: ").lower()
            if mode == 'e':
                result = vigenere_encrypt(text, key)
                print("Encrypted:", result)
            elif mode == 'd':
                result = vigenere_decrypt(text, key)
                print("Decrypted:", result)
            else:
                print("Unknown option.")

        elif choice == "3":
            print("\n--- Monoalphabetic Substitution Cipher ---")
            show_mono_key(mono_key)
            text = input("Enter text: ")
            mode = input("Type 'e' to encrypt, 'd' to decrypt: ").lower()
            if mode == 'e':
                result = mono_encrypt(text, mono_key)
                print("Encrypted:", result)
            elif mode == 'd':
                result = mono_decrypt(text, mono_key)
                print("Decrypted:", result)
            else:
                print("Unknown option.")

        elif choice == "4":
            print("\n--- XOR Cipher ---")
            text = input("Enter text: ")
            key = input("Enter key (short string, will repeat if shorter than text): ")
            mode = input("Type 'e' to encrypt, 'd' to decrypt: ").lower()
            if mode == 'e':
                result = xor_encrypt(text, key)
                # Show as bytes so students see non-printable characters
                print("Encrypted (raw):", result.encode())
            elif mode == 'd':
                # Accept raw bytes as input (for now, just treat as normal text)
                result = xor_decrypt(text, key)
                print("Decrypted:", result)
            else:
                print("Unknown option.")

        elif choice == "5":
            # Generate a new random monoalphabetic key
            mono_key = create_mono_key()
            print("New monoalphabetic key generated.")
            show_mono_key(mono_key)

        elif choice == "0":
            print("Goodbye! Remember: Crypto is only as strong as your key!")
            break
        else:
            print("Please enter a valid choice from the menu.")

if __name__ == "__main__":
    main()
