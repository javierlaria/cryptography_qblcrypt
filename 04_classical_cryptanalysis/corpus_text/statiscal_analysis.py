import string
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import entropy, pearsonr

# For color coding in terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Standard English letter frequencies (in percentages)
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
}

# English IC and Entropy approximations
ENGLISH_IC = 0.066
ENGLISH_ENTROPY = 4.2  # Approximate value for English text

def read_text(filename):
    """Read the content of a file and return it as uppercase, removing non-letter characters."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read().upper()
        # Remove non-letter characters
        text = ''.join([char for char in text if char in string.ascii_uppercase])
        return text
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        exit(1)

def compute_letter_counts(text):
    """Compute the count of each letter in the text."""
    counts = {letter: 0 for letter in string.ascii_uppercase}
    for char in text:
        counts[char] += 1
    return counts

def compute_frequencies(counts, total):
    """Compute the frequency percentages for each letter."""
    frequencies = {letter: (count / total * 100) if total > 0 else 0 for letter, count in counts.items()}
    return frequencies

def compute_ic(counts, total):
    """Compute the Index of Coincidence (IC)."""
    if total < 2:
        return 0.0
    ic = sum(count * (count - 1) for count in counts.values()) / (total * (total - 1))
    return ic

def compute_chi_squared(frequencies, total):
    """Compute the Chi-Squared statistic compared to English frequencies."""
    chi_sq = 0.0
    for letter in string.ascii_uppercase:
        observed = frequencies[letter] / 100 * total  # Convert back to count
        expected = ENGLISH_FREQ[letter] / 100 * total
        if expected > 0:
            chi_sq += (observed - expected) ** 2 / expected
    return chi_sq

def compute_entropy(frequencies):
    """Compute the Shannon entropy of the letter distribution."""
    probs = np.array([f / 100 for f in frequencies.values() if f > 0])
    if len(probs) == 0:
        return 0.0
    return entropy(probs, base=2)

def estimate_key_length(ic, total):
    """Estimate Vigenère key length using Friedman test (approximation)."""
    if ic <= 0.038 or total < 100:
        return "N/A (Insufficient data or too random)"
    kappa_p = 0.0665  # For English
    kappa_r = 1/26    # Random
    estimated_k = (kappa_p - kappa_r) / (ic - kappa_r)
    return round(estimated_k)

def color_code_ic(ic, label):
    """Color code IC based on proximity to English IC."""
    diff = abs(ic - ENGLISH_IC)
    if "Vigenère" in label or "polyalphabetic" in label.lower():
        # For polyalphabetic, lower IC expected
        if ic < 0.045:
            return Colors.GREEN + f"{ic:.4f}" + Colors.END
        elif ic < 0.055:
            return Colors.YELLOW + f"{ic:.4f}" + Colors.END
        else:
            return Colors.RED + f"{ic:.4f}" + Colors.END
    else:
        # For monoalphabetic or plaintext
        if diff < 0.005:
            return Colors.GREEN + f"{ic:.4f}" + Colors.END
        elif diff < 0.015:
            return Colors.YELLOW + f"{ic:.4f}" + Colors.END
        else:
            return Colors.RED + f"{ic:.4f}" + Colors.END

def color_code_chi_sq(chi_sq):
    """Color code Chi-Squared: lower is better (closer to English)."""
    if chi_sq < 50:
        return Colors.GREEN + f"{chi_sq:.2f}" + Colors.END
    elif chi_sq < 500:
        return Colors.YELLOW + f"{chi_sq:.2f}" + Colors.END
    else:
        return Colors.RED + f"{chi_sq:.2f}" + Colors.END

def color_code_entropy(ent):
    """Color code Entropy: around 4.2 for English."""
    diff = abs(ent - ENGLISH_ENTROPY)
    if diff < 0.2:
        return Colors.GREEN + f"{ent:.4f}" + Colors.END
    elif diff < 0.5:
        return Colors.YELLOW + f"{ent:.4f}" + Colors.END
    else:
        return Colors.RED + f"{ent:.4f}" + Colors.END

def interpret_results(label, ic, chi_sq, ent, key_len_est):
    """Provide senior cryptanalyst interpretation."""
    interpretation = f"\n{Colors.BOLD}Cryptanalyst Interpretation for {label}:{Colors.END}\n"
    
    if chi_sq < 50:
        interpretation += "- Chi-Squared is low: This text closely matches English letter distributions. Likely plaintext or decrypted.\n"
    elif chi_sq < 500:
        interpretation += "- Chi-Squared is moderate: Possible monoalphabetic substitution (e.g., Caesar). Try shifting to minimize Chi-Squared.\n"
    else:
        interpretation += "- Chi-Squared is high: Distribution far from English. Likely encrypted with polyalphabetic or other methods.\n"
    
    ic_diff = abs(ic - ENGLISH_IC)
    if ic_diff < 0.005:
        interpretation += "- IC close to English: Suggests monoalphabetic cipher or plaintext. Repetitions are natural.\n"
    elif ic < 0.045:
        interpretation += "- IC low: Indicates polyalphabetic cipher (e.g., Vigenère). Flattens frequencies.\n"
    else:
        interpretation += "- IC moderate: Could be partial decryption or mixed cipher. Further analysis needed.\n"
    
    if abs(ent - ENGLISH_ENTROPY) < 0.2:
        interpretation += "- Entropy normal for English: Low redundancy, typical of natural language.\n"
    elif ent > 4.5:
        interpretation += "- High Entropy: More uniform distribution, suggesting strong encryption or compression.\n"
    else:
        interpretation += "- Low Entropy: Highly repetitive, possibly weak encryption or non-English text.\n"
    
    if key_len_est != "N/A":
        interpretation += f"- Estimated Key Length: {key_len_est}. For Vigenère, use Kasiski or autocorrelation to confirm, then attack subgroups.\n"
    
    if "Caesar" in label:
        interpretation += "Recommendation: For Caesar, compute Chi-Squared for all 26 shifts; lowest indicates correct decryption.\n"
    elif "Vigenère" in label:
        interpretation += "Recommendation: Use estimated key length to divide text into cosets, analyze each with frequency analysis.\n"
    
    return interpretation

def print_frequencies(frequencies):
    """Print letter frequencies in a formatted way."""
    print("Letter Frequency (%):")
    letters = list(string.ascii_uppercase)
    for i in range(0, 26, 7):
        line = '  '.join([f"{letter}: {frequencies[letter]:.2f}%" for letter in letters[i:i+7]])
        print(line)

def plot_frequencies(frequencies, title, filename):
    """Plot the letter frequencies as a bar chart and save to file."""
    letters = list(string.ascii_uppercase)
    freq_values = [frequencies[letter] for letter in letters]
    eng_values = [ENGLISH_FREQ[letter] for letter in letters]

    plt.figure(figsize=(12, 6))
    x = np.arange(len(letters))
    width = 0.35

    plt.bar(x - width/2, freq_values, width, label='Text Frequencies')
    plt.bar(x + width/2, eng_values, width, label='English Frequencies')

    plt.xlabel('Letters')
    plt.ylabel('Frequency (%)')
    plt.title(f'Letter Frequency Distribution: {title}')
    plt.xticks(x, letters)
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.savefig(filename)
    plt.close()
    print(f"Frequency bar plot saved as '{filename}'")

def analyze_file(filename, label):
    """Perform full analysis on a file and return metrics."""
    text = read_text(filename)
    counts = compute_letter_counts(text)
    total = sum(counts.values())
    if total == 0:
        print(f"No letters found in {label}.")
        return None

    frequencies = compute_frequencies(counts, total)
    ic = compute_ic(counts, total)
    chi_sq = compute_chi_squared(frequencies, total)
    ent = compute_entropy(frequencies)
    key_len_est = estimate_key_length(ic, total) if "Vigenère" in label else "N/A"

    print("\n" + "=" * 40)
    print(f"Analysis for: {label}")
    print("=" * 40)
    print_frequencies(frequencies)
    print(f"Total letters: {total}")
    print(f"Index of Coincidence (IC): {color_code_ic(ic, label)} | Roughly 0.066 for natural English, near 0.038 for random/polyalphabetic text")
    print(f"Chi-Squared statistic vs. English letter frequencies: {color_code_chi_sq(chi_sq)} | Lower values indicate text closer to English norms")
    print(f"Shannon Entropy: {color_code_entropy(ent)} | Around 4.1-4.3 for English text")
    print(f"Estimated Key Length (if polyalphabetic): {key_len_est}")

    # Interpretation
    print(interpret_results(label, ic, chi_sq, ent, key_len_est))

    # Save bar plot
    plot_filename = f"{filename.split('.')[0]}_freq_bar.png"
    plot_frequencies(frequencies, label, plot_filename)

    return {
        'label': label,
        'frequencies': frequencies,
        'ic': ic,
        'chi_sq': chi_sq,
        'entropy': ent,
        'key_len_est': key_len_est,
        'total': total
    }

def advanced_visualizations(analyses):
    """Create Pandas DataFrame and advanced Seaborn visualizations."""
    if not analyses:
        return

    # Create DataFrame for frequencies
    letters = list(string.ascii_uppercase)
    freq_data = {'Letter': letters}
    for analysis in analyses:
        freq_data[analysis['label']] = [analysis['frequencies'][let] for let in letters]
    freq_df = pd.DataFrame(freq_data)

    # Add English frequencies for comparison
    freq_df['English Standard'] = [ENGLISH_FREQ[let] for let in letters]

    print("\n" + "=" * 40)
    print("Pandas DataFrame of Letter Frequencies:")
    print("=" * 40)
    print(freq_df.head(26))  # Show all rows

    # Save DataFrame to CSV
    freq_df.to_csv('letter_frequencies.csv', index=False)
    print("Letter frequencies saved to 'letter_frequencies.csv'")

    # Melt for seaborn plotting
    melted_df = pd.melt(freq_df, id_vars=['Letter'], var_name='Text', value_name='Frequency')

    # Set seaborn style
    sns.set(style="whitegrid", palette="muted")

    # Grouped Bar Plot
    plt.figure(figsize=(14, 8))
    sns.barplot(data=melted_df[melted_df['Text'] != 'English Standard'], x='Letter', y='Frequency', hue='Text')
    plt.title('Grouped Bar Plot of Letter Frequencies Across Texts')
    plt.savefig('grouped_bar_frequencies.png')
    plt.close()
    print("Grouped bar plot saved as 'grouped_bar_frequencies.png'")

    # Heatmap of Frequencies
    plt.figure(figsize=(12, 8))
    heatmap_data = freq_df.set_index('Letter').T
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
    plt.title('Heatmap of Letter Frequencies Across Texts and English Standard')
    plt.savefig('frequencies_heatmap.png')
    plt.close()
    print("Frequencies heatmap saved as 'frequencies_heatmap.png'")

    # Pie Charts (for top 10 letters per text, to avoid clutter)
    for analysis in analyses:
        top10 = sorted(analysis['frequencies'].items(), key=lambda x: x[1], reverse=True)[:10]
        labels, values = zip(*top10)
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f'Top 10 Letter Distribution Pie Chart: {analysis["label"]}')
        plt.savefig(f'{analysis["label"].replace(" ", "_")}_pie.png')
        plt.close()
        print(f"Pie chart saved as '{analysis['label'].replace(' ', '_')}_pie.png'")

    # Correlation Matrix between frequency distributions
    corr_matrix = freq_df.drop('Letter', axis=1).corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Frequency Distributions')
    plt.savefig('frequency_correlation_heatmap.png')
    plt.close()
    print("Correlation heatmap saved as 'frequency_correlation_heatmap.png'")

    # Additional Stats: Pearson Correlation with English
    print("\nPearson Correlation with English Standard:")
    eng_vec = freq_df['English Standard'].values
    for col in freq_df.columns[1:-1]:  # Exclude Letter and English
        text_vec = freq_df[col].values
        corr, _ = pearsonr(eng_vec, text_vec)
        print(f"{col}: {corr:.4f}")

    # Metrics DataFrame
    metrics_data = {
        'Text': [a['label'] for a in analyses],
        'IC': [a['ic'] for a in analyses],
        'Chi-Squared': [a['chi_sq'] for a in analyses],
        'Entropy': [a['entropy'] for a in analyses],
        'Estimated Key Length': [a['key_len_est'] for a in analyses]
    }
    metrics_df = pd.DataFrame(metrics_data)
    print("\n" + "=" * 40)
    print("Pandas DataFrame of Summary Metrics:")
    print("=" * 40)
    print(metrics_df)

    metrics_df.to_csv('summary_metrics.csv', index=False)
    print("Summary metrics saved to 'summary_metrics.csv'")

def main():
    print("=== Advanced Cryptanalysis Tool: Frequency, IC, Chi-Squared, Entropy, and Visualizations ===")
    print("Author: Pedro V. (Enhanced with Data Science Tools and Cryptanalysis Insights)")
    print("\nThis tool analyzes text files using statistical methods for cryptanalysis.")
    print(" - Computes letter frequencies, IC, Chi-Squared, Entropy.")
    print(" - Estimates key length for polyalphabetic ciphers.")
    print(" - Generates visualizations using Matplotlib and Seaborn.")
    print(" - Uses Pandas for data handling and SciPy for advanced stats.")
    print(" - Color-coded outputs: Green (good/close), Yellow (moderate), Red (far/off).")
    print(" - Includes senior cryptanalyst interpretations and recommendations.")

    original_file = input("\nEnter the filename for Original English file: ")
    caesar_file = input("Enter the filename for Caesar cipher file: ")
    vigenere_file = input("Enter the filename for Vigenère cipher file: ")

    analyses = []
    result = analyze_file(original_file, "Original English")
    if result: analyses.append(result)
    result = analyze_file(caesar_file, "Caesar Cipher")
    if result: analyses.append(result)
    result = analyze_file(vigenere_file, "Vigenère Cipher")
    if result: analyses.append(result)

    # Advanced Data Science Section
    advanced_visualizations(analyses)

if __name__ == "__main__":
    main()
