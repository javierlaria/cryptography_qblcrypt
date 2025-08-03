import math
import string

# --- Internal Single Columnar Transposition Functions ---
def _get_key_order(key):
    indexed_key = sorted([(key[i], i) for i in range(len(key))])
    return [index for char, index in indexed_key]

def _single_encrypt(plaintext, key):
    key_len = len(key)
    if key_len == 0: return plaintext
    read_order = _get_key_order(key)
    
    ciphertext = ""
    for col in read_order:
        pointer = col
        while pointer < len(plaintext):
            ciphertext += plaintext[pointer]
            pointer += key_len
    return ciphertext

def _single_decrypt(ciphertext, key):
    key_len = len(key)
    if key_len == 0: return ciphertext
    text_len = len(ciphertext)
    read_order = _get_key_order(key)

    num_rows = math.ceil(text_len / key_len)
    num_full_cols = text_len % key_len or key_len

    plaintext = ['_'] * text_len
    cipher_idx = 0

    for col_idx in read_order:
        col_len = num_rows - 1 if col_idx >= num_full_cols else num_rows
        for i in range(col_len):
            if cipher_idx < text_len:
                plaintext[col_idx + i * key_len] = ciphertext[cipher_idx]
                cipher_idx += 1
    return "".join(plaintext)

# --- Main Demo Functions ---
def welcome():
    print("=" * 60)
    print("🛡️  DOUBLE TRANSPOSITION CIPHER DEMO — by Pedro V")
    print("=" * 60)
    print("\n📖 A very strong classical cipher that applies the Columnar")
    print("   Transposition method TWICE with two different keys.")
    print("-" * 60)
    print("💡 Core idea: Plaintext -> Encrypt(Key1) -> Intermediate -> Encrypt(Key2) -> Final")
    print("   This process diffuses the letter patterns so well that it was")
    print("   a secure military field cipher for many decades.")
    print("\n   To decrypt, you must apply the keys in the REVERSE order:")
    print("   Final -> Decrypt(Key2) -> Intermediate -> Decrypt(Key1) -> Plaintext")
    print("-" * 60)

def encrypt(plaintext, key1, key2):
    """Encrypts using Double Transposition."""
    print("\nEncrypting...")
    padded_len1 = math.ceil(len(plaintext) / len(key1)) * len(key1)
    padded_text1 = plaintext.ljust(padded_len1, 'X')
    
    print(f"1. Encrypting with Key1 ('{key1}')...")
    intermediate_text = _single_encrypt(padded_text1, key1)
    print(f"   -> Intermediate Ciphertext: {intermediate_text}")

    padded_len2 = math.ceil(len(intermediate_text) / len(key2)) * len(key2)
    padded_text2 = intermediate_text.ljust(padded_len2, 'Z')
    
    print(f"\n2. Encrypting intermediate text with Key2 ('{key2}')...")
    final_ciphertext = _single_encrypt(padded_text2, key2)
    return final_ciphertext

def decrypt(ciphertext, key1, key2):
    """Decrypts using Double Transposition."""
    print("\nDecrypting...")
    print(f"1. Decrypting with Key2 ('{key2}')...")
    intermediate_text = _single_decrypt(ciphertext, key2)
    print(f"   -> Intermediate Plaintext: {intermediate_text}")

    print(f"\n2. Decrypting intermediate text with Key1 ('{key1}')...")
    final_plaintext = _single_decrypt(intermediate_text, key1)
    return final_plaintext.rstrip('XZ') # Remove padding

def run_brute_force_explanation():
    """Explains why brute-forcing this cipher is infeasible for a script."""
    print("\n--- Brute-Force Attack: A Lesson in Key Space ---")
    print("\nThis feature is for educational purposes to explain WHY this cipher is strong.")
    print("\n1. THE PROBLEM: A MASSIVE KEY SPACE")
    print("   - The Rail Fence cipher's key is a small number (2, 3, 4...). We can test them all in seconds.")
    print("   - The Double Transposition key is TWO separate words (e.g., 'SECRET' and 'CRYPTO').")
    
    print("\n2. THE MATH: WHY IT'S TOO SLOW")
    print("   - A small English dictionary has about 50,000 words.")
    print("   - To try every combination, we would need to test:")
    print("     50,000 (possible Key1s) * 50,000 (possible Key2s) = 2,500,000,000 combinations.")
    print("\n   - Even if we could test 1,000 keys per second, this would take over 28 days!")
    print("\n3. CONCLUSION")
    print("   - Simple brute force is not a viable way to break this cipher.")
    print("   - Real attacks require advanced statistical methods, far beyond the scope of this script.")
    print("   - This demonstrates the power of a large key space in making a cipher secure.")
    print("-" * 60)


def main():
    welcome()
    while True:
        print("\n" + "="*25 + " MENU " + "="*27)
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Brute-Force (Explanation)")
        print("4. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1' or choice == '2':
            key1 = input("Enter FIRST keyword: ").upper().replace(" ", "")
            key2 = input("Enter SECOND keyword: ").upper().replace(" ", "")
            if not key1 or not key2:
                print("Both keys are required.")
                continue

            if choice == '1':
                pt = input("Enter plaintext: ").upper().replace(" ", "")
                if pt:
                    ct = encrypt(pt, key1, key2)
                    print(f"\n🔒 Final Ciphertext: {ct}")
            else: # choice == '2'
                ct = input("Enter ciphertext: ").upper().replace(" ", "")
                if ct:
                    pt = decrypt(ct, key1, key2)
                    print(f"\n🔓 Final Plaintext: {pt}")

        elif choice == '3':
            run_brute_force_explanation()

        elif choice == '4':
            print("\nExiting the demo.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
