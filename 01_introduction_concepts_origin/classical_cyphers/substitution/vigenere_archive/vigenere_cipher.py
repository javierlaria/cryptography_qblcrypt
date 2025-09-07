# vigenere_cracker.py
# A Python program to crack a Vigenère cipher using Kasiski examination and frequency analysis.

import re
from collections import Counter

# --- Constants ---
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}
# A list of common English words to score the fitness of a decrypted text
COMMON_WORDS = ['THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT']

# --- Helper Functions ---

def clean_text(text):
    """Removes all non-alphabetic characters and converts to uppercase."""
    return re.sub(r'[^A-Z]', '', text.upper())

def find_repeated_sequences(text, min_len=3, max_len=5):
    """
    Finds repeated sequences in the text and the distances between them.
    This is the core of the Kasiski Examination.
    """
    sequences = {}
    for seq_len in range(min_len, max_len + 1):
        for i in range(len(text) - seq_len):
            seq = text[i:i+seq_len]
            if seq not in sequences:
                # Find all occurrences of this sequence
                indices = [m.start() for m in re.finditer(f'(?={seq})', text)]
                if len(indices) > 1:
                    sequences[seq] = indices
    
    distances = {}
    for seq, indices in sequences.items():
        for i in range(len(indices) - 1):
            dist = indices[i+1] - indices[i]
            if dist not in distances:
                distances[dist] = 0
            distances[dist] += 1
            
    return distances

def get_factors(number):
    """Returns a list of all factors for a given number."""
    factors = set()
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            factors.add(i)
            factors.add(number//i)
    return list(factors)

def find_likely_key_lengths(distances, max_results=5):
    """
    Analyzes the distances from Kasiski examination to find the most likely key lengths.
    """
    factor_counts = Counter()
    for dist, count in distances.items():
        factors = get_factors(dist)
        for factor in factors:
            # We are interested in key lengths, typically between 2 and 20
            if 2 <= factor <= 20:
                factor_counts[factor] += count
    
    # Return the most common factors, which are the most likely key lengths
    return [length for length, count in factor_counts.most_common(max_results)]

def get_nth_subcipher(key_length, n, text):
    """
    Extracts the n-th subcipher from the text for a given key length.
    For example, if key_length is 5, gets every 5th letter starting from the n-th letter.
    """
    return ''.join([text[i] for i in range(n, len(text), key_length)])

def frequency_analysis_attack(subcipher):
    """
    Performs a frequency analysis on a single subcipher (which is a Caesar cipher)
    to find the most likely key letter.
    """
    # Calculate the letter frequencies in the subcipher
    subcipher_len = len(subcipher)
    if subcipher_len == 0:
        return 'A' # Default if subcipher is empty
        
    freqs = {char: subcipher.count(char) / subcipher_len * 100 for char in ALPHABET}
    
    min_chi_squared = float('inf')
    best_shift = 0

    # Try all 26 possible shifts (for each letter of the alphabet as the key)
    for shift in range(26):
        chi_squared = 0.0
        # Calculate the Chi-Squared statistic for this shift
        for i, char in enumerate(ALPHABET):
            observed_char = ALPHABET[(i + shift) % 26]
            observed_freq = freqs.get(observed_char, 0)
            
            expected_freq = ENGLISH_FREQUENCIES.get(char, 0)
            
            # Chi-squared formula
            difference = observed_freq - expected_freq
            chi_squared += difference * difference / max(expected_freq, 1e-5) # Avoid division by zero
            
        if chi_squared < min_chi_squared:
            min_chi_squared = chi_squared
            best_shift = shift
            
    # The key letter corresponds to the best shift
    return ALPHABET[best_shift]

def vigenere_decrypt(ciphertext, key):
    """Decrypts Vigenère ciphertext with a known key."""
    key = key.upper()
    key_len = len(key)
    plaintext = ""
    key_index = 0
    
    for char in ciphertext.upper():
        if char in ALPHABET:
            key_char = key[key_index % key_len]
            key_shift = ALPHABET.find(key_char)
            
            cipher_index = ALPHABET.find(char)
            plain_index = (cipher_index - key_shift) % 26
            
            plaintext += ALPHABET[plain_index]
            key_index += 1
        else:
            # Keep non-alphabetic characters as they are
            plaintext += char
            
    return plaintext

def score_plaintext(text):
    """Scores a decrypted text based on the frequency of common English words."""
    score = 0
    for word in COMMON_WORDS:
        score += text.count(word)
    return score

# --- Main Cracking Function ---

def crack_vigenere(ciphertext):
    """
    Main function to orchestrate the cracking of a Vigenère cipher.
    """
    print("--- Starting Vigenère Cipher Analysis ---")
    
    # 1. Clean the ciphertext for analysis
    cleaned_text = clean_text(ciphertext)
    print(f"Analyzing {len(cleaned_text)} alphabetic characters.")

    # 2. Find repeated sequences and their distances (Kasiski Examination)
    distances = find_repeated_sequences(cleaned_text)
    if not distances:
        print("\n[Warning] No repeated sequences found. Kasiski examination is not effective.")
        print("This can happen on short texts. The tool may be less accurate.")
        # For very short texts, we might just have to guess common lengths
        likely_key_lengths = list(range(3, 8))
    else:
        # 3. Determine the most likely key lengths from the distances
        likely_key_lengths = find_likely_key_lengths(distances)
        if not likely_key_lengths:
             print("\n[Warning] Could not determine a likely key length. Guessing common lengths.")
             likely_key_lengths = list(range(3, 8))

    print(f"\nMost likely key lengths found: {likely_key_lengths}")

    best_key = ""
    best_plaintext = ""
    highest_score = -1

    # 4. For each likely key length, try to find the key and decrypt
    for key_len in likely_key_lengths:
        print(f"\n--- Testing Key Length: {key_len} ---")
        
        # 5. Build the key by attacking each subcipher
        potential_key = ""
        for i in range(key_len):
            subcipher = get_nth_subcipher(key_len, i, cleaned_text)
            key_letter = frequency_analysis_attack(subcipher)
            potential_key += key_letter
            
        print(f"Potential Key Found: {potential_key}")
        
        # 6. Decrypt the text with the potential key
        decrypted_text = vigenere_decrypt(ciphertext, potential_key)
        
        # 7. Score the result to see how "English-like" it is
        score = score_plaintext(decrypted_text)
        print(f"Decryption Score (higher is better): {score}")

        if score > highest_score:
            highest_score = score
            best_key = potential_key
            best_plaintext = decrypted_text

    # 8. Present the best result found
    print("\n--- Cracking Complete ---")
    print(f"Most likely key: {best_key}")
    print("\nDecrypted Plaintext:")
    print("="*40)
    print(best_plaintext)
    print("="*40)
    
    return best_key, best_plaintext

# --- Main Execution ---
if __name__ == '__main__':
    print("--- Vigenère Cipher Cracker ---")
    print("This program analyzes a ciphertext to find the keyword and decrypt the message.")
    print("Paste your Vigenère-encrypted message below and press Enter.")
    print("-" * 40)

    # Get input from the user
    ciphertext_input = input("Enter ciphertext: ")

    # Check if the user provided any input
    if not ciphertext_input.strip():
        print("\nNo ciphertext provided. Exiting.")
    else:
        crack_vigenere(ciphertext_input)

