# -*- coding: utf-8 -*-

def caesar_encrypt(text, shift):
    """
    Encrypts a text using the Caesar cipher.
    
    Each letter is shifted forward by a fixed number of positions in the alphabet.
    The modulo operator (%) ensures the shift wraps around the alphabet (e.g., 'Z' with shift 3 becomes 'C').
    Non-alphabetic characters are not changed.
    """
    result = ""
    for char in text:
        if char.isalpha(): # Check if the character is a letter
            # Determine the base ASCII value ('A' for uppercase, 'a' for lowercase)
            base = ord('A') if char.isupper() else ord('a')
            # Calculate the shifted character
            # 1. Get the character's 0-25 position in the alphabet (ord(char) - base)
            # 2. Add the shift
            # 3. Use modulo 26 to wrap around the alphabet
            # 4. Add the base back to get the new ASCII value
            # 5. Convert back to a character with chr()
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            # If not a letter, keep the character as is
            result += char
    return result

def caesar_decrypt(text, shift):
    """
    Decrypts a Caesar cipher text by shifting letters backward.
    This is equivalent to encrypting with a negative shift.
    """
    return caesar_encrypt(text, -shift)

def brute_force_attack(ciphertext):
    """
    Performs a brute-force attack on a Caesar-encrypted text.
    It tries every possible shift from 1 to 25 and prints the result.
    The user can then read the outputs to find the one that makes sense.
    """
    print("\n--- 🤖 Starting Brute-Force Attack ---")
    print("The Caesar cipher's main weakness is its tiny 'key space' (only 25 possible shifts).")
    print("We will now decrypt your text with every possible key. Look for the line that reveals a coherent message.")
    print("-" * 40)
    
    # The keyspace for a Caesar cipher is 1-25. A shift of 0 or 26 results in the original text.
    for shift_key in range(1, 26):
        # Decrypt the text with the current key guess
        potential_plaintext = caesar_decrypt(ciphertext, shift_key)
        # Use :02d to format the number with a leading zero for alignment (e.g., 01, 02, ...)
        print(f"Key #{shift_key:02d}: {potential_plaintext}")
    
    print("-" * 40)
    print("Attack complete. Did you find the original message?")

def run_interactive_cipher():
    """Main function to run the interactive cipher tool."""
    
    # --- Main Explanation ---
    print("="*60)
    print("🔑 Welcome to the Didactic Caesar Cipher Tool! 🔑")
    print("="*60)
    print("The Caesar cipher is a simple substitution cipher where each letter")
    print("in the plaintext is shifted a certain number of places down the alphabet.")
    print("\nFor example, with a 'shift' of 3:")
    print("  'A' becomes 'D'")
    print("  'Hello World!' becomes 'Khoor Zruog!'")
    print("\nThis script allows you to Encrypt, Decrypt, and even Brute-Force a message.")
    print("="*60)

    # --- Main Loop ---
    while True:
        # Prompt user for action
        action = input("\nChoose an action: (E)ncrypt, (D)ecrypt, (B)rute-force, or (Q)uit? ").strip().upper()

        if action == 'Q':
            print("Goodbye! 👋")
            break

        # --- ENCRYPTION ---
        if action == 'E':
            print("\n--- 🔒 Encryption Mode ---")
            text = input("Enter the text to encrypt: ")
            try:
                shift = int(input("Enter the shift value (a number from 1 to 25): "))
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be between 1 and 25.")
                
                encrypted_text = caesar_encrypt(text, shift)
                print(f"\nOriginal:   '{text}'")
                print(f"Encrypted:  '{encrypted_text}'")
                
                # Verification
                print(f"Verification (decrypting back): '{caesar_decrypt(encrypted_text, shift)}'")

            except ValueError as e:
                print(f"Error: Invalid input. {e}")

        # --- DECRYPTION ---
        elif action == 'D':
            print("\n--- 🗝️ Decryption Mode ---")
            text = input("Enter the text to decrypt: ")
            try:
                shift = int(input("Enter the shift value (the original key, 1-25): "))
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be between 1 and 25.")
                
                decrypted_text = caesar_decrypt(text, shift)
                print(f"\nCiphertext: '{text}'")
                print(f"Plaintext:  '{decrypted_text}'")

            except ValueError as e:
                print(f"Error: Invalid input. {e}")

        # --- BRUTE-FORCE ATTACK ---
        elif action == 'B':
            print("\n--- 💥 Brute-Force Mode ---")
            text = input("Enter the ciphertext to attack: ")
            brute_force_attack(text)

        else:
            print("Error: Invalid choice. Please enter 'E', 'D', 'B', or 'Q'.")

# Run the main program
if __name__ == "__main__":
    run_interactive_cipher()
