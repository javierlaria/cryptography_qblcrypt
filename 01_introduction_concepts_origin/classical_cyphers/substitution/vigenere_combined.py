# -*- coding: utf-8 -*-
# A combined tool for Vigenère cipher operations with a VERBOSE cracker.

import re
from collections import Counter
import sys

# --- Constants for Cracking ---
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}
COMMON_WORDS = ['THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'KEY', 'SECRET']

# --- Core Encryption/Decryption & Analysis ---
# (These functions are unchanged from the previous version)
def vigenere_cipher(text, key, mode='encrypt'):
    if not key.isalpha():
        print("[Error] Key must contain only alphabetic characters.")
        return None
    processed_text = []
    key = key.upper()
    key_length = len(key)
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            key_shift = ord(key[key_index % key_length]) - 65
            if mode == 'decrypt':
                key_shift = -key_shift
            processed_char_code = (ord(char) - offset + key_shift) % 26 + offset
            processed_text.append(chr(processed_char_code))
            key_index += 1
        else:
            processed_text.append(char)
    return ''.join(processed_text)

def analyze_key(key, plaintext):
    if not key.isalpha(): return
    key_len = len(key)
    plain_len = len(re.sub(r'[^a-zA-Z]', '', plaintext))
    keyspace = 26 ** key_len
    message_space = 26 ** plain_len
    complexity = ""
    if key.upper() in COMMON_WORDS:
        complexity = "Weak (This is a common dictionary word)"
    elif key_len <= 3: complexity = "Very Weak (Extremely short)"
    elif key_len <= 6: complexity = "Weak (Susceptible to modern cracking methods)"
    elif key_len <= 9: complexity = "Moderate (Offers reasonable resistance to manual analysis)"
    elif key_len <= 12: complexity = "Strong (Difficult to break without computers)"
    else: complexity = "Very Strong (Secure for its time)"
    print("\n" + "="*50)
    print("📈 Cryptographic Analysis".center(50))
    print("="*50)
    print("\n--- 🔑 KEYSPACE ---")
    print("The set of all possible keys.")
    print(f"Calculation: 26 ^ (key length) = 26^{key_len}")
    print(f"Total Keys:  {keyspace:,}")
    print(f"Key Strength: {complexity}")
    print("\n--- ✉️ MESSAGE SPACE ---")
    print("The set of all possible plaintexts of this message's length.")
    print(f"Calculation: 26 ^ (message length) = 26^{plain_len}")
    if plain_len > 50: print(f"Total Messages: A number with {len(str(message_space))} digits (too large to display!)")
    else: print(f"Total Messages: {message_space:,}")
    print("\n--- 🔒 CIPHERTEXT SPACE ---")
    print("The set of all possible encrypted messages of this length.")
    print(f"Calculation: 26 ^ (message length) = 26^{plain_len}")
    if plain_len > 50: print(f"Total Ciphertexts: A number with {len(str(message_space))} digits (identical to Message Space)")
    else: print(f"Total Ciphertexts: {message_space:,} (identical to Message Space)")
    print("\n" + "="*50)

# --- VERBOSE Cracker Helper Functions ---
def clean_text(text):
    return re.sub(r'[^A-Z]', '', text.upper())

def find_repeated_sequences(text, min_len=3, max_len=5):
    print("\n--- Finding Repeated Sequences (Kasiski Examination) ---")
    sequences = {}
    for seq_len in range(min_len, max_len + 1):
        for i in range(len(text) - seq_len):
            seq = text[i:i+seq_len]
            if seq not in sequences:
                indices = [m.start() for m in re.finditer(f'(?={seq})', text)]
                if len(indices) > 1:
                    sequences[seq] = indices
                    print(f"  Found sequence '{seq}' at positions: {indices}")
    
    distances = Counter()
    print("\n--- Calculating Distances Between Sequences ---")
    for seq, indices in sequences.items():
        for i in range(len(indices) - 1):
            dist = indices[i+1] - indices[i]
            distances[dist] += 1
            print(f"  Distance between '{seq}' occurrences: {dist}")
    return distances

def get_factors(number):
    factors = set()
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            factors.add(i)
            factors.add(number//i)
    return sorted(list(factors))

def find_likely_key_lengths(distances, max_results=5):
    print("\n--- Finding Common Factors of Distances ---")
    factor_counts = Counter()
    for dist, count in distances.items():
        factors = get_factors(dist)
        print(f"  Factors of distance {dist}: {factors}")
        for factor in factors:
            if 2 <= factor <= 20:
                factor_counts[factor] += count
    
    print("\n--- Tally of Potential Key Lengths (from factors) ---")
    if not factor_counts:
        return []
    for length, num_occurrences in factor_counts.most_common(max_results):
        print(f"  Key Length {length} occurred as a factor {num_occurrences} times.")
    return [length for length, count in factor_counts.most_common(max_results)]

def get_nth_subcipher(key_length, n, text):
    return ''.join([text[i] for i in range(n, len(text), key_length)])

def frequency_analysis_attack(subcipher):
    if not subcipher: return 'A'
    
    min_chi_squared = float('inf')
    best_key_letter = ''

    for key_letter in ALPHABET:
        shift = ALPHABET.find(key_letter)
        chi_squared = 0.0
        decrypted_subcipher = ''.join([ALPHABET[(ALPHABET.find(c) - shift) % 26] for c in subcipher])
        
        for char in ALPHABET:
            observed_count = decrypted_subcipher.count(char)
            expected_count = (ENGLISH_FREQUENCIES.get(char, 0) / 100) * len(decrypted_subcipher)
            difference = observed_count - expected_count
            chi_squared += difference * difference / max(expected_count, 1e-5)
            
        if chi_squared < min_chi_squared:
            min_chi_squared = chi_squared
            best_key_letter = key_letter
            
    print(f"    Best match is key letter '{best_key_letter}' (Chi-Squared: {min_chi_squared:.2f})")
    return best_key_letter

def score_plaintext(text):
    score = 0
    text_upper = text.upper()
    for word in COMMON_WORDS:
        score += text_upper.count(word)
    return score

# --- VERBOSE Main Cracking Orchestrator ---
def crack_vigenere(ciphertext):
    print("\n" + "="*60)
    print("🕵️  Starting Vigenère Cipher Analysis 🕵️".center(60))
    print("="*60)
    
    cleaned_text = clean_text(ciphertext)
    if not cleaned_text:
        print("\n[Error] No alphabetic characters found to analyze.")
        return

    # Phase 1: Find the key length
    distances = find_repeated_sequences(cleaned_text)
    if not distances:
        print("\n[Warning] No repeated sequences found. Guessing common key lengths.")
        likely_key_lengths = list(range(3, 10))
    else:
        likely_key_lengths = find_likely_key_lengths(distances)
        if not likely_key_lengths:
            print("\n[Warning] Kasiski analysis did not yield likely lengths. Guessing.")
            likely_key_lengths = list(range(3, 10))

    print(f"\n🏆 Most likely key lengths to test: {likely_key_lengths}")
    
    best_key = ""
    best_plaintext = ""
    highest_score = -1

    # Phase 2: Find the key letters
    for key_len in likely_key_lengths:
        print("\n" + "="*60)
        print(f"🔬 Testing Key Length: {key_len} 🔬".center(60))
        print("="*60)
        
        potential_key = ""
        for i in range(key_len):
            subcipher = get_nth_subcipher(key_len, i, cleaned_text)
            print(f"\n  Analyzing sub-cipher #{i+1} (every {key_len}th letter starting from position {i+1}):")
            print(f"  Sub-cipher Text: {subcipher[:60]}{'...' if len(subcipher) > 60 else ''}")
            print(f"  This is a simple Caesar cipher. We will now test all 26 possible shifts.")
            
            key_letter = frequency_analysis_attack(subcipher)
            potential_key += key_letter
            
        print("\n" + "-"*60)
        print(f"  Potential Key Found for length {key_len}: '{potential_key}'")
        
        decrypted_text = vigenere_cipher(ciphertext, potential_key, mode='decrypt')
        score = score_plaintext(decrypted_text)
        print(f"  Decryption Score (higher is better): {score}")

        if score > highest_score:
            highest_score = score
            best_key = potential_key
            best_plaintext = decrypted_text

    # Final Result
    print("\n" + "="*60)
    print("🏁 Cracking Complete 🏁".center(60))
    print("="*60)
    print(f"Most likely key based on scoring: '{best_key}'")
    print("\n--- Decrypted Plaintext ---")
    print(best_plaintext)
    print("-"*(len("--- Decrypted Plaintext ---")))

# --- Main Interactive Menu ---
def main():
    print("="*60)
    print("📜 Welcome to the All-in-One Vigenère Cipher Tool! 📜")
    print("="*60)
    while True:
        print("\nChoose an option:")
        choice = input("(E)ncrypt, (D)ecrypt, (C)rack, or (Q)uit? ").strip().upper()
        if choice == 'E':
            plaintext = input("Enter the text to encrypt: ")
            key = input("Enter the encryption key: ")
            analyze_key(key, plaintext) 
            encrypted = vigenere_cipher(plaintext, key, mode='encrypt')
            if encrypted:
                print("\n--- Encrypted Text ---")
                print(encrypted)
        elif choice == 'D':
            ciphertext = input("Enter the text to decrypt: ")
            key = input("Enter the decryption key: ")
            decrypted = vigenere_cipher(ciphertext, key, mode='decrypt')
            if decrypted:
                print("\n--- Decrypted Text ---")
                print(decrypted)
        elif choice == 'C':
            print("\nEnter the ciphertext to crack. For best results, use at least a few paragraphs.")
            ciphertext = input("Ciphertext: ")
            if not ciphertext.strip():
                print("\nNo ciphertext provided.")
            else:
                crack_vigenere(ciphertext)
        elif choice == 'Q':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
