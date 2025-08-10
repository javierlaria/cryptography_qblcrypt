import math
import string

def welcome():
    print("=" * 60)
    print("🏛️  COLUMNAR TRANSPOSITION CIPHER DEMO — by Pedro V")
    print("=" * 60)
    print("\n📖 This cipher rearranges letters based on a keyword.")
    print("   It offers much better security than the Rail Fence cipher.")
    print("-" * 60)
    print("💡 Core idea: Plaintext is written into a grid. The columns are")
    print("   then read out in an order determined by the alphabetized keyword.")
    print("\n   Plaintext:  WEAREDISCOVERED")
    print("   Keyword:    ZEBRA")
    print("\n   Z E B R A  (Alphabetical order: A, B, E, R, Z)")
    print("   5 2 1 4 3  <-- Numeric key based on letter order")
    print("   -----------")
    print("   W E A R E")
    print("   D I S C O")
    print("   V E R E D")
    print("\n   Ciphertext (reading columns 1, 2, 3, 4, 5): ASREDRDEOEVICW")
    print("-" * 60)

def get_key_order(key):
    """
    Derives the column order from the keyword.
    Example: KEY="ZEBRA" -> [4, 2, 1, 3, 0] -> Reads col 4, then 2, etc. (A,B,E,R,Z)
    Actually returns the read order of columns: [4, 1, 0, 3, 2]
    Correction: A simpler way is to find the order to READ the columns.
    KEY="ZEBRA" -> sorted is "ABERZ". 'A' is at index 4, 'B' is at index 2...
    So the read order is [col at 'A', col at 'B', ...] which is [4, 2, 1, 3, 0].
    Wait, let's simplify for implementation.
    KEY="ZEBRA", indexed: [('Z',0), ('E',1), ('B',2), ('R',3), ('A',4)]
    Sorted: [('A',4), ('B',2), ('E',1), ('R',3), ('Z',0)]
    Read order of columns: [4, 2, 1, 3, 0]
    """
    indexed_key = sorted([(key[i], i) for i in range(len(key))])
    read_order = [index for char, index in indexed_key]
    return read_order

def print_grid(plaintext, key):
    """Prints a visual representation of the columnar grid."""
    print("\nVisualizing the grid:")
    key_len = len(key)
    # Padded for perfect grid
    padded_len = math.ceil(len(plaintext) / key_len) * key_len
    padded_text = plaintext.ljust(padded_len, '_')
    
    order = get_key_order(key)
    # Create a map from column index to its rank (1st, 2nd, etc.)
    rank_map = {col_index: rank + 1 for rank, col_index in enumerate(order)}

    print("   " + " ".join(key))
    print("   " + " ".join(str(rank_map[i]) for i in range(key_len)))
    print("  " + "-" * (key_len * 2))

    for i in range(0, padded_len, key_len):
        print(" | " + " ".join(padded_text[i:i+key_len]))
    print()


def encrypt(plaintext, key):
    """Encrypts a message using the Columnar Transposition cipher."""
    key_len = len(key)
    read_order = get_key_order(key)
    print_grid(plaintext, key)
    
    ciphertext = ""
    for col in read_order:
        pointer = col
        while pointer < len(plaintext):
            ciphertext += plaintext[pointer]
            pointer += key_len
            
    return ciphertext

def decrypt(ciphertext, key):
    """Decrypts a message from the Columnar Transposition cipher."""
    key_len = len(key)
    text_len = len(ciphertext)
    read_order = get_key_order(key)

    num_rows = math.ceil(text_len / key_len)
    num_full_cols = text_len % key_len or key_len # If 0, all cols are full

    plaintext = ['_'] * text_len
    cipher_idx = 0

    # Reconstruct the grid column by column
    for col_idx in read_order:
        # Determine if this column is one of the shorter ones
        col_len = num_rows - 1 if col_idx >= num_full_cols else num_rows
        
        for i in range(col_len):
            plaintext[col_idx + i * key_len] = ciphertext[cipher_idx]
            cipher_idx += 1
            
    return "".join(plaintext)

def main():
    welcome()
    while True:
        print("\n--- MENU ---\n1. Encrypt\n2. Decrypt\n3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            pt = input("Enter plaintext: ").upper().replace(" ", "")
            key = input("Enter keyword: ").upper().replace(" ", "")
            if pt and key:
                ct = encrypt(pt, key)
                print(f"\n🔒 Ciphertext: {ct}")
        elif choice == '2':
            ct = input("Enter ciphertext: ").upper().replace(" ", "")
            key = input("Enter keyword: ").upper().replace(" ", "")
            if ct and key:
                pt = decrypt(ct, key)
                print(f"\n🔓 Plaintext: {pt}")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

