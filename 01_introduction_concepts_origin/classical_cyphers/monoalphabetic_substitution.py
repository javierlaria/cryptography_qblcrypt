# -*- coding: utf-8 -*-
import random
import string
import re
from collections import Counter

# --- Global variable for the dictionary ---
ENGLISH_WORDS = set()

# --- Core Cipher Functions ---
def generate_key():
    """Generates a random key (a shuffled alphabet map)."""
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def apply_cipher(text, key_map):
    """Applies a substitution to the text using the provided key map."""
    result = ""
    if not key_map:
        return text
    for char in text:
        if char.isalpha():
            # Use '?' to denote letters that are not yet in the key map
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

# --- Automatic Solver Functions ---
def load_dictionary():
    """Loads words from 'words.txt' into a set for fast lookups."""
    try:
        with open('words.txt', 'r') as f:
            return {word.strip().lower() for word in f}
    except FileNotFoundError:
        return None

def get_word_pattern(word):
    """Generates a pattern for a word, e.g., 'hello' -> 'ABCCB'."""
    pattern = ""
    mapping = {}
    next_char_code = 0
    for char in word.lower():
        if char not in mapping:
            mapping[char] = str(next_char_code)
            next_char_code += 1
        pattern += mapping[char]
    return pattern

def solve_recursively(words, key):
    """The main recursive solver."""
    if not words:
        return key

    word_to_solve = words[0]
    remaining_words = words[1:]
    pattern = get_word_pattern(word_to_solve)
    
    possible_matches = []
    for dict_word in ENGLISH_WORDS:
        if get_word_pattern(dict_word) == pattern:
            consistent = True
            for i in range(len(word_to_solve)):
                cipher_char, plain_char = word_to_solve[i], dict_word[i]
                if (cipher_char in key and key[cipher_char] != plain_char) or \
                   (plain_char in key.values() and cipher_char not in key):
                    consistent = False
                    break
            if consistent:
                possible_matches.append(dict_word)

    for match in possible_matches:
        new_key = key.copy()
        for i in range(len(word_to_solve)):
            new_key[word_to_solve[i]] = match[i]
        
        solution = solve_recursively(remaining_words, new_key)
        if solution is not None:
            return solution
            
    return None

def run_solver(ciphertext):
    """Initializes and runs the automatic solver with a transparent analysis step."""
    print("\n" + "="*60)
    print("🤖 Automatic Cipher Solver 🤖")
    print("="*60)

    if not ENGLISH_WORDS:
        print("Error: 'words.txt' not found or is empty.")
        return

    print("--- 🔍 Initial Analysis: Detective's Notebook ---")
    words = sorted(list(set(re.findall(r'\b[a-zA-Z]+\b', ciphertext.lower()))), key=len, reverse=True)
    
    print(f"{'Ciphertext Word':<20} {'Pattern'}")
    print(f"{'-'*19:<20} {'-'*7}")
    for word in words:
        print(f"{word:<20} {get_word_pattern(word)}")
    
    print("\n" + "-"*60)
    print("Analysis complete. Now attempting to find a solution recursively...")
    print("This may take a moment.\n")
    
    final_key = solve_recursively(words, {})
    
    if final_key:
        decrypted_text = apply_cipher(ciphertext, final_key)
        print("--- ✅ Solution Found! ---")
        print(f"\nDecrypted Text: {decrypted_text}")
    else:
        print("--- ❌ Solution Not Found ---")

# --- Main Interactive Program ---
def run_interactive_tool():
    """Main function to run the interactive cipher tool."""
    global ENGLISH_WORDS
    ENGLISH_WORDS = load_dictionary()

    print("="*60)
    print("📜 Welcome to the All-in-One Monoalphabetic Cipher Tool! 📜")
    print("="*60)
    
    session_key = generate_key()

    while True:
        print("\n" + "-"*60)
        print("Current Key (first few letters): a->{}, b->{}, c->{}, ...".format(session_key['a'], session_key['b'], session_key['c']))
        action = input("Choose: (E)ncrypt, (D)ecrypt, (S)olve, (N)ew Key, or (Q)uit? ").strip().upper()

        if action == 'Q':
            print("Goodbye! 👋")
            break
        
        elif action == 'N':
            session_key = generate_key()
            print("✨ A new random key has been generated for this session.")
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
            ciphertext = input("Enter the ciphertext to solve: ")
            run_solver(ciphertext)

        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    run_interactive_tool()
