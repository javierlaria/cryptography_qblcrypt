# Author: Pedro V.
# Complete Vigenère Analysis with Detailed Comparison & Repeats Viewer

import re
from collections import defaultdict, Counter
import string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
import math

init(autoreset=True)

LANGUAGE_FREQUENCIES = {
    'english': {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
        'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
        'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
        'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
        'Y': 1.974, 'Z': 0.074
    },
    'french': {
        'A': 7.636, 'B': 0.901, 'C': 3.260, 'D': 3.669, 'E': 14.715, 'F': 1.066,
        'G': 0.866, 'H': 0.737, 'I': 7.529, 'J': 0.545, 'K': 0.049, 'L': 5.456,
        'M': 2.968, 'N': 7.095, 'O': 5.796, 'P': 2.521, 'Q': 1.362, 'R': 6.553,
        'S': 7.948, 'T': 7.244, 'U': 6.311, 'V': 1.628, 'W': 0.114, 'X': 0.387,
        'Y': 0.308, 'Z': 0.136
    },
    'spanish': {
        'A': 11.72, 'B': 1.49, 'C': 3.87, 'D': 4.67, 'E': 13.72, 'F': 0.69,
        'G': 1.00, 'H': 1.18, 'I': 5.28, 'J': 0.52, 'K': 0.11, 'L': 5.24,
        'M': 3.08, 'N': 6.83, 'O': 8.44, 'P': 2.89, 'Q': 1.11, 'R': 6.41,
        'S': 7.20, 'T': 4.60, 'U': 4.55, 'V': 1.05, 'W': 0.04, 'X': 0.14,
        'Y': 1.09, 'Z': 0.47
    }
}

def clean_text(text):
    """Removes non-alphabetic characters and converts to uppercase."""
    return ''.join([c.upper() for c in text if c.upper() in string.ascii_uppercase])

def kasiski_examination(text, min_seq_len=3, report_limit=10, all_repeats=False):
    """Finds repeated sequences in the text and calculates distances between them."""
    seq_positions = defaultdict(list)
    for seq_len in range(min_seq_len, 6):
        for i in range(len(text) - seq_len):
            seq = text[i:i+seq_len]
            seq_positions[seq].append(i)
    
    repeats = []
    for seq, positions in seq_positions.items():
        if len(positions) > 1:
            for j in range(1, len(positions)):
                dist = positions[j] - positions[j-1]
                repeats.append((seq, positions[j-1], positions[j], dist))
    
    if not all_repeats:
        print(Fore.YELLOW + "\nFound repeated sequences (showing first {}):".format(report_limit))
        for seq, pos1, pos2, dist in repeats[:report_limit]:
            print(Fore.YELLOW + f"  '{seq}' at positions {pos1} → {pos2} (distance: {dist})")
        if len(repeats) > report_limit:
            print(Fore.YELLOW + f"  ... ({len(repeats)} repeats in total)")
            
    return repeats

def gcd_list(numbers):
    """Calculates the greatest common divisor (GCD) of a list of numbers."""
    from math import gcd
    if not numbers:
        return 1
    result = numbers[0]
    for n in numbers[1:]:
        result = gcd(result, n)
    return result

def friedman_test(text):
    """Performs the Friedman test to estimate key length."""
    char_counts = Counter(text)
    N = len(text)
    ic_numerator = sum(count * (count - 1) for count in char_counts.values())
    ic_observed = ic_numerator / (N * (N - 1)) if N > 1 else 0
    
    numerator = 0.027 * N
    denominator = (N - 1) * ic_observed - 0.038 * N + 0.065
    estimated_key_length = numerator / denominator if denominator > 0 else None
    
    return ic_observed, estimated_key_length

def split_by_period(text, period):
    """Splits the ciphertext into columns based on the period."""
    columns = [''] * period
    for i, c in enumerate(text):
        columns[i % period] += c
    return columns

def index_of_coincidence(column):
    """Calculates the Index of Coincidence for a given text column."""
    freq = Counter(column)
    N = len(column)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1)) if N > 1 else 0
    return ic

def ic_period_analysis(text, max_period=20):
    """Analyzes periods by calculating the average Index of Coincidence."""
    results = []
    for period in range(2, max_period + 1):
        cols = split_by_period(text, period)
        avg_ic = sum(index_of_coincidence(col) for col in cols) / period
        results.append({'Period': period, 'Avg_IC': avg_ic, 'Distance_from_English': abs(avg_ic - 0.065)})
    
    ic_df = pd.DataFrame(results)
    best_period_ic = ic_df.loc[ic_df['Distance_from_English'].idxmin()]
    
    print(Fore.YELLOW + "\nPeriod analysis results (top 10 candidates):")
    print(Fore.WHITE + "| Period | Avg IC | Distance from English IC |")
    print(Fore.WHITE + "|--------|--------|---------------------------|")
    top_candidates = ic_df.nsmallest(10, 'Distance_from_English')
    for _, row in top_candidates.iterrows():
        highlight = Fore.GREEN if row['Period'] == best_period_ic['Period'] else Fore.WHITE
        print(f"{highlight}|    {int(row['Period']):2}    | {row['Avg_IC']:.4f} |          {row['Distance_from_English']:.4f}           |")
        
    return int(best_period_ic['Period']), ic_df

def caesar_decrypt(text, shift):
    """Decrypts a text using a Caesar cipher shift."""
    result = ""
    for char in text:
        if char in string.ascii_uppercase:
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            result += char
    return result

def chi_squared_test(text, language_freqs):
    """Calculates the Chi-squared statistic for a given text against language frequencies."""
    observed = Counter(text)
    total = len(text)
    chi2 = 0
    for letter in string.ascii_uppercase:
        observed_count = observed.get(letter, 0)
        expected_count = (language_freqs[letter] / 100) * total
        if expected_count > 0:
            chi2 += ((observed_count - expected_count) ** 2) / expected_count
    return chi2

def analyze_column(column, language_freqs, column_num):
    """Finds the best Caesar shift for a single column using Chi-squared analysis."""
    print(Fore.CYAN + f"\n[INFO] Analyzing column {column_num + 1} (length: {len(column)})...")
    print(Fore.YELLOW + f"Column text preview: {column[:20]}{'...' if len(column) > 20 else ''}")
    
    best_shift = 0
    best_chi2 = float('inf')
    results = []
    
    for shift in range(26):
        decrypted = caesar_decrypt(column, shift)
        chi2 = chi_squared_test(decrypted, language_freqs)
        results.append({'Shift': shift, 'Chi2': chi2, 'Key_Letter': chr(shift + ord('A'))})
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_shift = shift
            
    results_df = pd.DataFrame(results).sort_values('Chi2')
    
    print(Fore.GREEN + f"Top 3 key candidates for column {column_num + 1}:")
    print(Fore.WHITE + "| Rank | Key Letter | Shift | Chi² Score |")
    print(Fore.WHITE + "|------|------------|-------|------------|")
    for i, (_, row) in enumerate(results_df.head(3).iterrows()):
        rank_color = Fore.GREEN if row['Shift'] == best_shift else Fore.WHITE
        print(f"{rank_color}|   {i+1:2}   |      {row['Key_Letter']}     |   {int(row['Shift']):2}   |   {row['Chi2']:8.2f}   |")
        
    return chr(best_shift + ord('A')), best_shift, best_chi2

def decrypt_vigenere(ciphertext, key):
    """Decrypts a Vigenère-encrypted text with a given key."""
    decrypted = []
    key_upper = key.upper()
    key_len = len(key_upper)
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            key_char = key_upper[i % key_len]
            shift = ord(key_char) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def evaluate_decryption_quality(text):
    """Evaluates the quality of a decrypted text based on linguistic properties."""
    if not text:
        return {'vowel_ratio': 0, 'ic': 0, 'pattern_score': 0, 'quality_score': 0}
        
    vowel_count = sum(1 for c in text if c in 'AEIOU')
    vowel_ratio = vowel_count / len(text) if len(text) > 0 else 0
    ic = index_of_coincidence(text)
    
    common_patterns = ['THE', 'AND', 'ING', 'ION', 'TIO', 'ENT', 'FOR']
    pattern_score = sum(text.count(pattern) for pattern in common_patterns)
    
    return {
        'vowel_ratio': vowel_ratio,
        'ic': ic,
        'pattern_score': pattern_score,
        'quality_score': ic * 10 + vowel_ratio * 5 + pattern_score * 0.1
    }

def perform_frequency_analysis(text, period, language_freqs):
    """Performs frequency analysis for a given period to find the key."""
    columns = split_by_period(text, period)
    key_letters = []
    total_chi2 = 0
    
    print(Fore.MAGENTA + Style.BRIGHT + f"\n=== FREQUENCY ANALYSIS (Period: {period}) ===")
    for i, column in enumerate(columns):
        key_letter, shift, chi2 = analyze_column(column, language_freqs, i)
        key_letters.append(key_letter)
        total_chi2 += chi2
        
    recovered_key = ''.join(key_letters)
    decrypted = decrypt_vigenere(text, recovered_key)
    quality = evaluate_decryption_quality(decrypted)
    
    print(Fore.MAGENTA + Style.BRIGHT + 
          f"\n=== RESULTS FOR PERIOD {period} ===\n"
          f"🔑 Recovered Key: '{recovered_key}'\n"
          f"📊 Total Chi² Score: {total_chi2:.2f}\n"
          f"🎯 Quality Score: {quality['quality_score']:.2f}\n"
          f"📈 Index of Coincidence: {quality['ic']:.4f}\n"
          f"🗣️ Vowel Ratio: {quality['vowel_ratio']:.3f}")
          
    return recovered_key, decrypted, total_chi2, quality

def main():
    """Main function to run the Vigenère cryptanalysis suite."""
    print(Fore.MAGENTA + Style.BRIGHT + "=== COMPLETE VIGENÈRE CRYPTANALYSIS SUITE ===")
    print(Fore.MAGENTA + "🔍 Kasiski + Friedman + IC Analysis + Manual Period Testing")
    print(Fore.CYAN + "Author: Pedro V\n")
    
    fn = input("Enter the filename of your Vigenère-encrypted text: ").strip()
    try:
        with open(fn, "r", encoding="utf8") as f:
            raw = f.read()
    except FileNotFoundError:
        print(Fore.RED + f"Could not find file '{fn}'.")
        return
        
    text = clean_text(raw)
    print(Fore.GREEN + f"\n[INFO] Loaded {len(text)} characters for analysis.")
    
    # Automatic analysis
    kasiski_repeats = kasiski_examination(text)
    kasiski_distances = [dist for _, _, _, dist in kasiski_repeats]
    observed_ic, friedman_estimate = friedman_test(text)
    ic_best_period, ic_df = ic_period_analysis(text)
    
    # Get language choice
    print(Fore.CYAN + Style.BRIGHT + "\n=== LANGUAGE SELECTION ===")
    print(Fore.WHITE + "Available languages: English, French, Spanish")
    while True:
        lang_choice = input("Select language for frequency analysis (english/french/spanish): ").lower().strip()
        if lang_choice in LANGUAGE_FREQUENCIES:
            break
        print(Fore.RED + "Invalid choice. Please enter 'english', 'french', or 'spanish'.")
    language_freqs = LANGUAGE_FREQUENCIES[lang_choice]
    
    # Show automatic suggestion
    print(Fore.CYAN + Style.BRIGHT + f"\n=== AUTOMATIC ANALYSIS SUGGESTS ===")
    if friedman_estimate is not None:
        print(Fore.CYAN + f"📊 Friedman Test: ~{round(friedman_estimate)} characters")
    print(Fore.CYAN + f"📈 IC Analysis: {ic_best_period} characters")
    if kasiski_distances:
        gcd_result = gcd_list(kasiski_distances)
        print(Fore.CYAN + f"🔍 Kasiski GCD: {gcd_result} characters")
        
    # Try the automatic suggestion first
    print(Fore.YELLOW + f"\n[INFO] Testing automatic suggestion: period {ic_best_period}")
    auto_key, auto_decrypted, auto_chi2, auto_quality = perform_frequency_analysis(text, ic_best_period, language_freqs)
    
    print(Fore.GREEN + Style.BRIGHT + "\n=== 📜 DECRYPTED TEXT PREVIEW (first 200 characters) ===")
    print(Fore.WHITE + auto_decrypted[:200] + ("..." if len(auto_decrypted) > 200 else ""))
    
    # Interactive period testing
    tried_periods = {ic_best_period: (auto_key, auto_decrypted, auto_chi2, auto_quality)}
    
    while True:
        print(Fore.CYAN + Style.BRIGHT + "\n=== PERIOD TESTING OPTIONS ===")
        print(Fore.WHITE + "1. Try a different period length")
        print(Fore.WHITE + "2. Compare all tested periods")
        print(Fore.WHITE + "3. Show all repeated sequences (Kasiski)")
        print(Fore.WHITE + "4. Save current best result and exit")
        choice = input("Your choice (1/2/3/4): ").strip()
        
        if choice == '1':
            try:
                new_period = int(input("Enter period length to test (2-25): "))
                if 2 <= new_period <= 25:
                    if new_period in tried_periods:
                        print(Fore.YELLOW + f"Period {new_period} already tested. Here are the results:")
                        key, decrypted, chi2, quality = tried_periods[new_period]
                        print(Fore.MAGENTA + f"Key: '{key}', Quality Score: {quality['quality_score']:.2f}")
                        print(Fore.WHITE + decrypted[:200] + ("..." if len(decrypted) > 200 else ""))
                    else:
                        print(Fore.YELLOW + f"\n[INFO] Testing period {new_period}...")
                        key, decrypted, chi2, quality = perform_frequency_analysis(text, new_period, language_freqs)
                        tried_periods[new_period] = (key, decrypted, chi2, quality)
                        print(Fore.GREEN + Style.BRIGHT + "\n=== 📜 DECRYPTED TEXT PREVIEW ===")
                        print(Fore.WHITE + decrypted[:200] + ("..." if len(decrypted) > 200 else ""))
                else:
                    print(Fore.RED + "Please enter a period between 2 and 25.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
                
        elif choice == '2':
            if tried_periods:
                print(Fore.CYAN + Style.BRIGHT + "\n=== COMPARISON OF TESTED PERIODS ===")
                print(Fore.WHITE + "| Period | Key          | Chi² Score | Quality Score | IC     |")
                print(Fore.WHITE + "|--------|--------------|------------|---------------|--------|")
                
                sorted_periods = sorted(tried_periods.items(), key=lambda x: x[1][3]['quality_score'], reverse=True)
                # FIX: Iterate over values and access the quality dictionary at index 3.
                best_quality_score = max(item[3]['quality_score'] for item in tried_periods.values())

                for period, (key, decrypted, chi2, quality) in sorted_periods:
                    highlight = Fore.GREEN if quality['quality_score'] == best_quality_score else Fore.WHITE
                    print(f"{highlight}|   {period:2}   | {key:<12} | {chi2:10.2f} | {quality['quality_score']:13.2f} | {quality['ic']:.4f} |")
            else:
                print(Fore.RED + "No periods tested yet.")
                
        elif choice == '3':
            print(Fore.CYAN + Style.BRIGHT + "\n=== ALL REPEATED SEQUENCES (KASISKI) ===")
            for seq, pos1, pos2, dist in kasiski_repeats:
                print(Fore.WHITE + f"'{seq}' at positions {pos1} → {pos2} (distance: {dist})")
            print(Fore.GREEN + f"Total repeated sequences found: {len(kasiski_repeats)}")
            
        elif choice == '4':
            if tried_periods:
                best_period_data = max(tried_periods.items(), key=lambda x: x[1][3]['quality_score'])
                period, (key, decrypted, chi2, quality) = best_period_data
                
                print(Fore.GREEN + Style.BRIGHT + 
                      f"\n=== 🎉 FINAL RESULTS 🎉 ===\n"
                      f"🏆 Best Period: {period}\n"
                      f"🔑 Final Key: '{key}'\n"
                      f"📊 Quality Score: {quality['quality_score']:.2f}")
                      
                with open("decrypted_output.txt", "w") as f:
                    f.write(decrypted)
                print(Fore.CYAN + f"[INFO] Full decrypted text saved to 'decrypted_output.txt'")
                print(Fore.GREEN + Style.BRIGHT + "🎯 Cryptanalysis complete!")
                break
            else:
                print(Fore.RED + "No results to save.")
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

