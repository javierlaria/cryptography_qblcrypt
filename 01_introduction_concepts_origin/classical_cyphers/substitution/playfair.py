# Playfair Cipher Implementation for Classroom Demo
# Demonstrates substitution cipher with digraphs using a 5x5 key square
# No file I/O or network calls; pure Python for teaching

def create_key_square(passphrase):
    """Generate a 5x5 key square from a passphrase."""
    # Remove spaces, punctuation, and convert to uppercase; merge I/J
    passphrase = ''.join(c.upper() for c in passphrase if c.isalpha()).replace('J', 'I')
    
    # Remove duplicates, keeping first occurrence
    seen = set()
    key = [c for c in passphrase if not (c in seen or seen.add(c))]
    
    # Add remaining alphabet (excluding J, as I/J are merged)
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for c in alphabet:
        if c not in seen:
            key.append(c)
    
    # Create 5x5 grid (list of 5 lists, each with 5 letters)
    square = [key[i:i+5] for i in range(0, 25, 5)]
    
    # Print square for students to see
    print("\nKey Square:")
    for row in square:
        print(' '.join(row))
    return square

def find_position(square, letter):
    """Find row, col of a letter in the 5x5 square."""
    for row in range(5):
        for col in range(5):
            if square[row][col] == letter:
                return row, col
    return None  # Shouldn't happen with valid input

def prepare_text(text):
    """Prepare plaintext: uppercase, remove non-letters, split into digraphs."""
    # Convert to uppercase, remove non-letters, replace J with I
    text = ''.join(c.upper() for c in text if c.isalpha()).replace('J', 'I')
    
    # Insert X between double letters and at end if odd length
    i = 0
    digraphs = []
    while i < len(text):
        if i + 1 < len(text):
            if text[i] == text[i + 1]:  # Double letter, insert X
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        else:  # Odd length, add X
            digraphs.append(text[i] + 'X')
            i += 1
    
    print("\nDigraphs:", digraphs)
    return digraphs

def playfair_encrypt(square, digraphs):
    """Encrypt digraphs using Playfair rules."""
    ciphertext = []
    
    for pair in digraphs:
        row1, col1 = find_position(square, pair[0])
        row2, col2 = find_position(square, pair[1])
        
        if row1 == row2:  # Same row: shift right
            ciphertext.append(square[row1][(col1 + 1) % 5] + square[row2][(col2 + 1) % 5])
        elif col1 == col2:  # Same column: shift down
            ciphertext.append(square[(row1 + 1) % 5][col1] + square[(row2 + 1) % 5][col2])
        else:  # Rectangle: swap corners
            ciphertext.append(square[row1][col2] + square[row2][col1])
    
    return ''.join(ciphertext)

def playfair_decrypt(square, digraphs):
    """Decrypt digraphs using Playfair rules (reverse directions)."""
    plaintext = []
    
    for pair in digraphs:
        row1, col1 = find_position(square, pair[0])
        row2, col2 = find_position(square, pair[1])
        
        if row1 == row2:  # Same row: shift left
            ciphertext.append(square[row1][(col1 - 1) % 5] + square[row2][(col2 - 1) % 5])
        elif col1 == col2:  # Same column: shift up
            ciphertext.append(square[(row1 - 1) % 5][col1] + square[(row2 - 1) % 5][col2])
        else:  # Rectangle: swap corners (same as encrypt)
            ciphertext.append(square[row1][col2] + square[row2][col1])
    
    return ''.join(ciphertext)

def main():
    """Main function to run Playfair cipher demo."""
    print("=== Playfair Cipher Demo ===")
    
    # Get user input
    passphrase = input("Enter passphrase (e.g., 'MONARCHY'): ").strip()
    if not any(c.isalpha() for c in passphrase):
        print("Error: Passphrase must contain at least one letter!")
        return
    
    mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
    if mode not in ['encrypt', 'decrypt']:
        print("Error: Please choose 'encrypt' or 'decrypt'.")
        return
    
    message = input("Enter message (letters only, J treated as I): ").strip()
    if not any(c.isalpha() for c in message):
        print("Error: Message must contain at least one letter!")
        return
    
    # Create key square
    square = create_key_square(passphrase)
    
    # Prepare digraphs
    digraphs = prepare_text(message)
    
    # Encrypt or decrypt
    if mode == 'encrypt':
        result = playfair_encrypt(square, digraphs)
        print("\nEncrypted message:", result)
    else:
        result = playfair_decrypt(square, digraphs)
        print("\nDecrypted message:", result)
        print("Note: Remove any trailing 'X' for final plaintext.")

if __name__ == "__main__":
    main()
