# -*- coding: utf-8 -*-
import string
import re
import sys

# --- Configuration ---
# The path to your dictionary file, as you provided.
# Make sure this file exists, or the solver will not work.
DICTIONARY_FILE_PATH = '/home/qblcrypt/github_repos/cryptography_qblcrypt/01_introduction_concepts_origin/classical_cyphers/words.txt'

# --- Global variables ---
# This will hold a pre-computed map of patterns to words for massive speed improvements.
# e.g., {'0.1.2.2.1': ['hello', 'sells', ...]}
PATTERN_MAP = {}
ENGLISH_WORDS = set()

# --- Dictionary and Pattern Functions ---

def load_dictionary(filepath):
    """
    Loads the dictionary file and pre-computes the PATTERN_MAP.
    This is the most crucial step for performance.
    """
    global ENGLISH_WORDS, PATTERN_MAP
    try:
        with open(filepath, 'r') as f:
            # We use a set for fast 'in' checks.
            ENGLISH_WORDS = {word.strip().lower() for word in f}

        # Pre-computation: Group all dictionary words by their pattern.
        for word in ENGLISH_WORDS:
            pattern = get_word_pattern(word)
            if pattern not in PATTERN_MAP:
                PATTERN_MAP[pattern] = []
            PATTERN_MAP[pattern].append(word)

        print(f"✅ Dictionary '{filepath}' loaded successfully.")
        print(f"   ({len(ENGLISH_WORDS)} words and {len(PATTERN_MAP)} unique patterns found)")
        return True
    except FileNotFoundError:
        print(f"❌ CRITICAL ERROR: Dictionary file not found at '{filepath}'.")
        print("   Please check the path in the DICTIONARY_FILE_PATH variable.")
        return False
    except Exception as e:
        print(f"An error occurred while loading the dictionary: {e}")
        return False

def get_word_pattern(word):
    """
    Generates a numeric pattern for a word.
    e.g., 'hello' -> '0.1.2.2.1'
           'sells' -> '0.1.2.2.0' (typo in thinking, should be 0.1.2.2.3) let's correct it -> 'sells' -> '0.1.2.2.3'
           'apple' -> '0.1.1.2.3'
    """
    word = word.lower()
    next_num = 0
    letter_nums = {}
    pattern = []
    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        pattern.append(letter_nums[letter])
    return '.'.join(pattern)

# --- Core Cipher & Solver Functions ---

def generate_key():
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    # For simplicity, we just need a stub function here.
    return dict(zip(letters, shuffled))

def display_key(key):
    print("--- 🔑 Deduced Substitution Key ---")
    plaintext_alpha = " ".join(string.ascii_lowercase)
    ciphertext_alpha = " ".join([key.get(c, '?') for c in string.ascii_lowercase])
    print(f"Plaintext:  {plaintext_alpha}\n            {'| ' * 26}\nCiphertext: {ciphertext_alpha}")

def decrypt_with_partial_key(ciphertext, key):
    """Applies a key (Ciphertext -> Plaintext) to decrypt a message."""
    inverse_key = {v: k for k, v in key.items()}
    plaintext = ''
    for char in ciphertext:
        if char.lower() in key:
            sub = key[char.lower()]
            plaintext += sub.upper() if char.isupper() else sub
        elif char.isalpha():
            plaintext += '?' # Unsolved letters
        else:
            plaintext += char
    return plaintext

def solve_recursively(cipher_words, key):
    """
    The main backtracking solver.
    """
    if not cipher_words:
        # Base case: All words have been solved. We found a valid key.
        return key

    # Heuristic: Solve the longest words first as they have fewer possible matches.
    current_word = max(cipher_words, key=len)
    remaining_words = cipher_words - {current_word}
    
    pattern = get_word_pattern(current_word)
    candidate_words = PATTERN_MAP.get(pattern, [])

    for candidate in candidate_words:
        # 1. Create a potential new key from this candidate match.
        new_key = key.copy()
        is_consistent = True
        
        # 2. Check for contradictions with the existing key.
        for i, cipher_char in enumerate(current_word):
            plain_char = candidate[i]
            if cipher_char in new_key and new_key[cipher_char] != plain_char:
                is_consistent = False; break # Contradiction 1
            if plain_char in new_key.values() and new_key.get(cipher_char) != plain_char:
                is_consistent = False; break # Contradiction 2
            new_key[cipher_char] = plain_char

        if not is_consistent:
            continue # This candidate doesn't work, try the next one.
        
        # 3. If consistent, try to solve the rest of the message.
        solution = solve_recursively(remaining_words, new_key)
        
        if solution is not None:
            # Success! A solution was found down this path.
            return solution
            
    # 4. If we loop through all candidates and none lead to a solution, backtrack.
    return None

def run_solver(ciphertext):
    """Initializes and runs the dictionary-based solver."""
    print("\n" + "="*70)
    print("🧩 Automatic Cipher Solver: Dictionary Pattern Matching 🧩")
    print("="*70)

    if not PATTERN_MAP:
        print("Solver cannot run because the dictionary and pattern map are not loaded.")
        return

    # Extract unique, alphabetic words from the ciphertext.
    cipher_words = set(re.findall(r'\b[a-zA-Z]+\b', ciphertext.lower()))
    if not cipher_words:
        print("No valid words found in the ciphertext to solve.")
        return

    print("Found the following encrypted words to analyze:")
    print(f"  {', '.join(sorted(list(cipher_words), key=len, reverse=True))}")
    print("\nAttempting to find a unique solution... This may take a moment.")
    
    # Kick off the recursive solver with an empty key.
    final_key = solve_recursively(cipher_words, {})
    
    print("\n" + "-"*70)
    if final_key:
        print("✅ Solution Found!")
        # For display, create the Plaintext -> Ciphertext version
        displayable_key = {v: k for k, v in final_key.items()}
        display_key(displayable_key)
        
        print("\n--- Decrypted Message ---")
        decrypted_text = decrypt_with_partial_key(ciphertext, final_key)
        print(decrypted_text)
    else:
        print("❌ Solution Not Found.")
        print("   This could happen if the message contains non-dictionary words,")
        print("   is too short, or the dictionary is missing key words.")
    print("="*70)

# --- Main Interactive Program ---
def main():
    """Main function to run the interactive tool."""
    if not load_dictionary(DICTIONARY_FILE_PATH):
        sys.exit(1) # Exit if the dictionary can't be loaded.

    print("\n" + "="*60)
    print("📜 Dictionary-Based Substitution Cipher Tool 📜")
    print("="*60)
    
    while True:
        action = input("\nChoose: (S)olve Ciphertext, or (Q)uit? ").strip().upper()

        if action == 'Q':
            print("Goodbye! 👋")
            break
        elif action == 'S':
            ciphertext = input("\nEnter the ciphertext to solve:\n> ")
            run_solver(ciphertext)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
