import math
import string
from collections import defaultdict

def welcome():
    print("=" * 60)
    print("🇵🇱 MYSZKOWSKI TRANSPOSITION CIPHER DEMO — by Pedro V")
    print("=" * 60)
    print("\n📖 A variation of Columnar Transposition with a special rule")
    print("   for keywords that have repeated letters.")
    print("-" * 60)
    print("💡 Core idea: Columns under unique letters are read normally.")
    print("   Columns under REPEATED letters are read left-to-right.")
    print("\n   Plaintext:  THEQUICKBROWNFOX")
    print("   Keyword:    TOMORROW")
    print("\n   T O M O R R O W  (Numeric key: 4 2 1 2 3 3 2 5)")
    print("   -----------------")
    print("   T H E Q U I C K")
    print("   B R O W N F O X")
    print("\n   Ciphertext: EOB HROW TQNF CIKXU") # By rank M, O, R, T, W
    print("-" * 60)

def get_key_map(key):
    """
    Groups column indices by key character.
    Example: TOMORROW -> {'T':[0], 'O':[1,3,6], 'M':[2], 'R':[4,5], 'W':[7]}
    """
    key_map = defaultdict(list)
    for i, char in enumerate(key):
        key_map[char].append(i)
    return key_map

def encrypt(plaintext, key):
    """Encrypts using Myszkowski Transposition."""
    print("\nEncrypting...")
    key_len = len(key)
    num_rows = math.ceil(len(plaintext) / key_len)
    
    # Pad plaintext to fill grid
    padded_text = plaintext.ljust(num_rows * key_len, '_')
    
    key_map = get_key_map(key)
    sorted_unique_chars = sorted(key_map.keys())
    
    ciphertext = ""
    for char in sorted_unique_chars:
        columns_to_read = key_map[char]
        if len(columns_to_read) == 1: # Normal columnar read
            col = columns_to_read[0]
            for i in range(num_rows):
                ciphertext += padded_text[i * key_len + col]
        else: # Myszkowski horizontal read
            for i in range(num_rows):
                for col in columns_to_read:
                    ciphertext += padded_text[i * key_len + col]
    return ciphertext

def decrypt(ciphertext, key):
    """Decrypts using Myszkowski Transposition."""
    print("\nDecrypting...")
    key_len = len(key)
    text_len = len(ciphertext)
    num_rows = math.ceil(text_len / key_len)
    
    # Create grid to fill
    grid = ['_'] * (num_rows * key_len)
    
    key_map = get_key_map(key)
    sorted_unique_chars = sorted(key_map.keys())
    
    cipher_idx = 0
    # Reverse of encryption: place characters back into the grid
    for char in sorted_unique_chars:
        columns_to_read = key_map[char]
        block_len = len(columns_to_read) * num_rows
        
        block = ciphertext[cipher_idx : cipher_idx + block_len]
        cipher_idx += block_len
        
        block_ptr = 0
        if len(columns_to_read) == 1: # Normal columnar fill
            col = columns_to_read[0]
            for i in range(num_rows):
                grid[i * key_len + col] = block[block_ptr]
                block_ptr += 1
        else: # Myszkowski de-interleaving
            for i in range(num_rows):
                for col in columns_to_read:
                    grid[i * key_len + col] = block[block_ptr]
                    block_ptr += 1
                    
    return "".join(grid).rstrip('_')

def main():
    welcome()
    while True:
        print("\n--- MENU ---\n1. Encrypt\n2. Decrypt\n3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            pt = input("Enter plaintext: ").upper().replace(" ", "")
            key = input("Enter keyword (use repeated letters): ").upper().replace(" ", "")
            if pt and key:
                ct = encrypt(pt, key)
                print(f"\n🔒 Ciphertext: {ct}")
        elif choice == '2':
            ct = input("Enter ciphertext: ").upper().replace(" ", "")
            key = input("Enter keyword (with repeated letters): ").upper().replace(" ", "")
            if ct and key:
                pt = decrypt(ct, key)
                print(f"\n🔓 Plaintext: {pt}")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
