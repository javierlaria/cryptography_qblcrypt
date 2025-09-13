# -*- coding: utf-8 -*-
import random
import string
import re
from collections import Counter

# --- Constants for Frequency Analysis ---
# The standard frequency of letters in the English language, from most to least common.
ENGLISH_LETTER_FREQUENCY = 'etaoinshrdlcumwfgypbvkjxqz'

# --- Core Cipher Functions ---
def generate_key():
    """Generates a random key (a shuffled alphabet map)."""
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def display_key(key):
    """Displays the full substitution key in a clear, readable format."""
    print("--- 🔑 Current Substitution Key ---")
    plaintext_alpha = " ".join(string.ascii_lowercase)
    # This function expects a key where Plaintext -> Ciphertext
    ciphertext_alpha = " ".join([key.get(c, '?') for c in string.ascii_lowercase])
    
    print(f"Plaintext:  {plaintext_alpha}")
    print(f"            {'| ' * 26}")
    print(f"Ciphertext: {ciphertext_alpha}")
    print("-" * 34)

def apply_cipher(text, key_map):
    """Applies a substitution to the text using the provided key map."""
    result = ""
    if not key_map:
        return text
    for char in text:
        if char.isalpha():
            # For decryption, this expects a key where Ciphertext -> Plaintext
            sub_char = key_map.get(char.lower(), '?')
            result += sub_char.upper() if char.isupper() else sub_char
        else:
            result += char
    return result

def encrypt(text, key):
    """Encrypts text using the given key."""
    return apply_cipher(text, key)

def decrypt(text, key):
    """Decrypts text by applying an inverted key."""
    inverse_key = {v: k for k, v in key.items()}
    return apply_cipher(text, inverse_key)

# --- Automatic Solver using Frequency Analysis ---
def get_ciphertext_frequency(ciphertext):
    """Calculates the frequency of each letter in the ciphertext."""
    text_only_letters = re.sub(r'[^a-zA-Z]', '', ciphertext).lower()
    counts = Counter(text_only_letters)
    sorted_by_freq = sorted(counts, key=counts.get, reverse=True)
    return ''.join(sorted_by_freq)

def run_solver(ciphertext):
    """Breaks the cipher using frequency analysis."""
    print("\n" + "="*60)
    print("🤖 Automatic Cipher Solver (Frequency Analysis) 🤖")
    print("="*60)

    if not ciphertext.strip():
        print("Error: Cannot solve an empty ciphertext.")
        return

    # 1. Calculate the frequency of letters in the provided ciphertext
    ciphertext_freq_order = get_ciphertext_frequency(ciphertext)
    
    print("--- 🔍 Frequency Analysis ---")
    print("Most common letters found in ciphertext:")
    print(f"  '{ciphertext_freq_order}'")
    print("\nStandard English letter frequency:")
    print(f"  '{ENGLISH_LETTER_FREQUENCY}'")

    # 2. Build the Ciphertext -> Plaintext key for decryption
    likely_key_for_decryption = {}
    for i, cipher_char in enumerate(ciphertext_freq_order):
        if i < len(ENGLISH_LETTER_FREQUENCY):
            plain_char = ENGLISH_LETTER_FREQUENCY[i]
            likely_key_for_decryption[cipher_char] = plain_char

    # To display the key correctly, we need to invert it to Plaintext -> Ciphertext format
    # because that's what the display_key function expects.
    displayable_key = {v: k for k, v in likely_key_for_decryption.items()}
    
    print("\n--- 🧠 Derived Key ---")
    print("Mapping ciphertext letters to plaintext based on frequency:")
    display_key(displayable_key) # Pass the correctly formatted key

    # 3. Apply the derived key to get a proposed decryption
    # The decryption itself uses the original (non-inverted) key.
    decrypted_text = apply_cipher(ciphertext, likely_key_for_decryption)
    
    print("--- 🎯 Decryption Attempt ---")
    print("This is a best guess. Some letters may need to be swapped manually.")
    print(f"\nCiphertext:     '{ciphertext}'")
    print(f"Decrypted Text: '{decrypted_text}'")
    print("="*60)


# --- Main Interactive Program ---
def run_interactive_tool():
    """Main function to run the interactive cipher tool."""
    print("="*60)
    print("📜 Welcome to the All-in-One Monoalphabetic Cipher Tool! 📜")
    print("="*60)
    
    session_key = generate_key()

    while True:
        print("\n")
        display_key(session_key)
        action = input("Choose: (E)ncrypt, (D)ecrypt, (S)olve, (N)ew Key, or (Q)uit? ").strip().upper()

        if action == 'Q':
            print("Goodbye! 👋")
            break
        
        elif action == 'N':
            session_key = generate_key()
            print("\n✨ A new random key has been generated for this session.")
            continue

        elif action == 'E':
            print("\n--- 🔒 Encryption ---")
            plaintext = input("Enter the text to encrypt: ")
            ciphertext = encrypt(plaintext, session_key)
            print(f"\nPlaintext:  '{plaintext}'")
            print(f"Ciphertext: '{ciphertext}'")

        elif action == 'D':
            print("\n--- 🗝️ Decryption ---")
            ciphertext = input("Enter the text to decrypt (using the current key): ")
            decrypted_text = decrypt(ciphertext, session_key)
            print(f"\nCiphertext: '{ciphertext}'")
            print(f"Plaintext:  '{decrypted_text}'")

        elif action == 'S':
            ciphertext = input("\nEnter the ciphertext to solve: ")
            run_solver(ciphertext)

        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    run_interactive_tool()
