# -*- coding: utf-8 -*-
import random
import string
import re
from collections import Counter

# --- Constants for Cryptanalysis ---
# Standard frequency of letters in English
ENGLISH_LETTER_FREQUENCY = 'etaoinshrdlcumwfgypbvkjxqz'

# Most common two-letter pairs (digrams) in English
ENGLISH_DIGRAMS = [
    'th', 'he', 'in', 'er', 'an', 're', 'es', 'on', 'st', 'nt', 
    'en', 'at', 'ed', 'to', 'or', 'ea', 'hi', 'is', 'ou', 'ar'
]
# Most common three-letter groups (trigrams) in English
ENGLISH_TRIGRAMS = [
    'the', 'and', 'ing', 'her', 'ere', 'ent', 'tha', 'nth', 'was', 
    'eth', 'for', 'dth', 'ion', 'tio', 'ter', 'est'
]

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
    ciphertext_alpha = " ".join([key.get(c, '?') for c in string.ascii_lowercase])
    
    print(f"Plaintext:  {plaintext_alpha}")
    print(f"            {'| ' * 26}")
    print(f"Ciphertext: {ciphertext_alpha}")
    print("-" * 34)

def apply_cipher(text, key_map):
    """Applies a substitution to the text using the provided key map."""
    result = ""
    if not key_map: return text
    for char in text:
        if char.isalpha():
            sub_char = key_map.get(char.lower(), '❓')
            result += sub_char.upper() if char.isupper() else sub_char
        else:
            result += char
    return result

def encrypt(text, key):
    return apply_cipher(text, key)

def decrypt(text, key):
    inverse_key = {v: k for k, v in key.items()}
    return apply_cipher(text, inverse_key)

# --- New In-Depth Automatic Solver ---

def get_ngram_frequency(text, n):
    """Generic function to get the frequency of n-grams (n=1, 2, or 3)."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    ngrams = []
    for word in words:
        for i in range(len(word) - n + 1):
            ngrams.append(word[i:i+n])
    
    counts = Counter(ngrams)
    return counts.most_common()

def run_solver(ciphertext):
    """Breaks the cipher using a detailed, multi-step analysis."""
    print("\n" + "="*70)
    print("🕵️  Automatic Cipher Solver: In-Depth Cryptanalysis 🕵️")
    print("="*70)
    print("\nWelcome, students! We're going to solve this like detectives,")
    print("gathering clues from three different sources before making our final guess.")
    
    if not ciphertext.strip():
        print("\n[ERROR] Cannot solve an empty ciphertext.")
        return

    # --- 1. Monogram (Single Letter) Analysis ---
    print("\n\n--- 🔍 Clue #1: Single Letter Frequencies ---")
    print("First, let's count every single letter in the ciphertext.")
    
    text_only_letters = re.sub(r'[^a-zA-Z]', '', ciphertext).lower()
    total_letters = len(text_only_letters)
    letter_counts = Counter(text_only_letters)
    
    print(f"\n{'Cipher Letter':<15} {'Count':>5}   {'Frequency (%)':>15}")
    print(f"{'-'*15:<15} {'-'*5:>5}   {'-'*15:>15}")
    
    sorted_cipher_letters = letter_counts.most_common()
    ciphertext_freq_order = ''.join([item[0] for item in sorted_cipher_letters])
    
    for letter, count in sorted_cipher_letters:
        percentage = (count / total_letters) * 100
        print(f"{letter:<15} {count:>5}   {percentage:>14.2f}%")

    # Build the first-guess key based on this
    monogram_key = {}
    for i, cipher_char in enumerate(ciphertext_freq_order):
        if i < len(ENGLISH_LETTER_FREQUENCY):
            monogram_key[cipher_char] = ENGLISH_LETTER_FREQUENCY[i]

    # --- 2. Digram (Two-Letter Pair) Analysis ---
    print("\n\n--- 🔍 Clue #2: Two-Letter Pair (Digram) Frequencies ---")
    print("Letters often travel in pairs. Let's find the most common pairs.")
    
    top_cipher_digrams = [item[0] for item in get_ngram_frequency(ciphertext, 2)[:10]]
    
    print("\nMost common pairs in the Ciphertext:")
    print(f"  {', '.join(top_cipher_digrams)}")
    print("\nMost common pairs in English:")
    print(f"  {', '.join(ENGLISH_DIGRAMS[:10])}")
    print("\nThis suggests potential mappings. For example, if 'iq' is common in the")
    print("ciphertext, it might correspond to 'th' in English.")

    # --- 3. Trigram (Three-Letter Group) Analysis ---
    print("\n\n--- 🔍 Clue #3: Three-Letter Group (Trigram) Frequencies ---")
    print("Powerful patterns emerge in groups of three, like the word 'the'.")

    top_cipher_trigrams = [item[0] for item in get_ngram_frequency(ciphertext, 3)[:5]]
    
    print("\nMost common triplets in the Ciphertext:")
    print(f"  {', '.join(top_cipher_trigrams)}")
    print("\nMost common triplets in English:")
    print(f"  {', '.join(ENGLISH_TRIGRAMS[:5])}")
    print("\nThis is our strongest clue! If 'dqv' is the top ciphertext trigram,")
    print("it is very likely the word 'the'. This gives us three letters at once!")

    # --- 4. Synthesizing the Clues to Build a Refined Key ---
    print("\n\n--- 🧠 The Deduction: Building a Smarter Key ---")
    print("Now, let's combine all our clues to make an educated guess.")
    
    refined_key = monogram_key.copy()
    
    # Use Trigrams first as they are the most reliable clue
    top_cipher_tri = get_ngram_frequency(ciphertext, 3)
    if top_cipher_tri:
        cipher_t, cipher_h, cipher_e = top_cipher_tri[0][0]
        # Very strong assumption: top trigram is 'the'
        refined_key[cipher_t] = 't'
        refined_key[cipher_h] = 'h'
        refined_key[cipher_e] = 'e'
        print("Clue applied: The most common trigram was mapped to 'the'.")
    
    # (Optional: Add more logic for digrams if needed, but trigrams are often enough)
    
    # --- 5. The Solution ---
    print("\n--- 🎯 The Final Decryption Attempt ---")
    
    # Create the key for display (Plaintext -> Ciphertext)
    displayable_key = {v: k for k, v in refined_key.items()}
    display_key(displayable_key)

    decrypted_text = apply_cipher(ciphertext, refined_key)
    
    print("\nBased on our analysis, here is the best guess:")
    print(f"\nCiphertext:     '{ciphertext}'")
    print(f"Decrypted Text: '{decrypted_text}'")
    print("\nNotice how many words are now readable! From here, a human could")
    print("easily spot the last few mistakes and swap letters to solve it completely.")
    print("="*70)


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

        if action == 'Q': print("Goodbye! 👋"); break
        elif action == 'N':
            session_key = generate_key()
            print("\n✨ A new random key has been generated for this session.")
        elif action == 'E':
            print("\n--- 🔒 Encryption ---")
            plaintext = input("Enter the text to encrypt: ")
            print(f"\nPlaintext:  '{plaintext}'\nCiphertext: '{encrypt(plaintext, session_key)}'")
        elif action == 'D':
            print("\n--- 🗝️ Decryption ---")
            ciphertext = input("Enter the text to decrypt (using the current key): ")
            print(f"\nCiphertext: '{ciphertext}'\nPlaintext:  '{decrypt(ciphertext, session_key)}'")
        elif action == 'S':
            ciphertext = input("\nEnter the ciphertext to solve: ")
            run_solver(ciphertext)
        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    run_interactive_tool()
