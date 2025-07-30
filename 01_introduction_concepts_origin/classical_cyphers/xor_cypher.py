# -*- coding: utf-8 -*-
import os
import string

# --- Constants for Cryptanalysis ---
ENGLISH_IC = 0.067
EXPECTED_BYTES = set(bytes(string.ascii_letters + string.digits + string.punctuation + ' ', 'utf-8'))

# --- Core Cipher Functions ---

def xor_operation(data: bytes, key: bytes) -> bytes:
    """Performs a repeating-key XOR operation on byte data."""
    if not key: return data # Return data if key is empty
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# --- Cryptanalysis (Attack) Functions ---

def get_index_of_coincidence(data: bytes) -> float:
    """Calculates the Index of Coincidence (IC) for a block of data."""
    n = len(data)
    if n < 2: return 0.0
    counts = [0] * 256
    for byte in data: counts[byte] += 1
    numerator = sum(count * (count - 1) for count in counts)
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0.0

def find_key_length(ciphertext: bytes, max_len: int = 40) -> int:
    """Finds the most likely key length using the Index of Coincidence."""
    best_len = 0
    closest_ic_avg = float('inf')

    for key_len in range(2, min(max_len, len(ciphertext) // 2) + 1):
        columns = [ciphertext[i::key_len] for i in range(key_len)]
        avg_ic = sum(get_index_of_coincidence(col) for col in columns) / key_len
        
        if abs(avg_ic - ENGLISH_IC) < abs(closest_ic_avg - ENGLISH_IC):
            closest_ic_avg = avg_ic
            best_len = key_len
            
    return best_len

def solve_single_byte_xor(column: bytes) -> int:
    """Finds the most likely single-byte key for a column of data."""
    best_score = -1
    best_key_byte = 0
    
    for key_guess in range(256):
        decrypted = xor_operation(column, bytes([key_guess]))
        score = sum(1 for byte in decrypted if byte in EXPECTED_BYTES)
        
        if score > best_score:
            best_score = score
            best_key_byte = key_guess
            
    return best_key_byte

def run_attack(ciphertext: bytes):
    """Runs the full attack pipeline against a repeating-key XOR ciphertext."""
    print("\n" + "="*60)
    print("💥 Repeating-Key XOR Attack 💥")
    print("="*60)
    
    key_len = find_key_length(ciphertext)
    if key_len == 0:
        print("❌ Could not determine a likely key length. The text may be too short.")
        return
    print(f"✅ Step 1: Most likely key length found: {key_len}")

    columns = [ciphertext[i::key_len] for i in range(key_len)]
    solved_key_bytes = [solve_single_byte_xor(col) for col in columns]
    solved_key = bytes(solved_key_bytes)
    
    print(f"✅ Step 2: Solved key: '{solved_key.decode(errors='ignore')}'")

    decrypted_text = xor_operation(ciphertext, solved_key).decode(errors='ignore')
    print("-" * 60)
    print("--- 🔓 Decrypted Message ---")
    print(decrypted_text)

# --- OTP Encryption Function ---
def run_otp_encryption():
    """Demonstrates a secure One-Time Pad encryption."""
    print("\n" + "="*60)
    print("✨ One-Time Pad (OTP) Encryption ✨")
    print("="*60)
    print("This mode demonstrates PERFECT secrecy by following the three OTP rules:")
    print("1. The key is **truly random** (using os.urandom).")
    print("2. The key is the **same length as the message**.")
    print("3. The key is for **ONE-TIME USE ONLY**.")
    
    plaintext = input("\nEnter the plaintext to encrypt: ")
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Generate a cryptographically secure random key of the same length
    key_bytes = os.urandom(len(plaintext_bytes))
    
    ciphertext_bytes = xor_operation(plaintext_bytes, key_bytes)
    
    print("\n--- Results ---")
    print(f"Plaintext: {plaintext}")
    print(f"ONE-TIME PAD KEY (hex): {key_bytes.hex()}")
    print(f"Ciphertext (hex):       {ciphertext_bytes.hex()}")
    print("\n" + "-"*60)
    print("⚠️  IMPORTANT: To decrypt, the recipient needs the EXACT key shown above.")
    print("This key must never be used again. An attack on this ciphertext is futile.")


# --- Main Interactive Program ---
def run_interactive_tool():
    """Main function to run the interactive XOR cipher tool."""
    print("="*60)
    print("🔑 Welcome to the Didactic XOR Cipher Tool! 🔑")
    print("="*60)
    print("Learn the difference between a weak repeating-key XOR and the unbreakable One-Time Pad.")

    while True:
        print("\n" + "-"*60)
        action = input("Choose: (E)ncrypt (Repeating Key), (O)TP Encrypt, (D)ecrypt, (A)ttack, or (Q)uit? ").strip().upper()

        if action == 'Q':
            print("Goodbye! 👋")
            break
        
        if action == 'E': # Standard, weak repeating-key XOR
            text_input = input("Enter the plaintext to encrypt: ")
            key_input = input("Enter the repeating key (e.g., 'SECRET'): ")
            try:
                result = xor_operation(text_input.encode('utf-8'), key_input.encode('utf-8'))
                print(f"\n✅ Encrypted Ciphertext (hex): {result.hex()}")
            except Exception as e:
                print(f"\n❌ Error: {e}")

        elif action == 'O': # One-Time Pad
            run_otp_encryption()
            
        elif action == 'D': # Decryption works for both
            hex_ciphertext = input("Enter the ciphertext (in hex format) to decrypt: ")
            key_input = input("Enter the key (as text or hex): ")
            try:
                # Try to decode key as hex first, otherwise treat as text
                try:
                    key_bytes = bytes.fromhex(key_input)
                except ValueError:
                    key_bytes = key_input.encode('utf-8')
                
                data_bytes = bytes.fromhex(hex_ciphertext)
                result = xor_operation(data_bytes, key_bytes)
                print(f"\n✅ Decrypted Plaintext: {result.decode(errors='ignore')}")
            except (ValueError, TypeError) as e:
                print(f"\n❌ Error: Invalid input. Ensure ciphertext is a valid hex string. Details: {e}")

        elif action == 'A':
            hex_ciphertext = input("Enter the repeating-key ciphertext (in hex format) to attack: ")
            try:
                ciphertext_bytes = bytes.fromhex(hex_ciphertext)
                run_attack(ciphertext_bytes)
            except ValueError:
                print("\n❌ Error: Invalid hex string provided.")
        
        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    run_interactive_tool()
