def vigenere_encrypt(plaintext, key):
    encrypted = []
    key = key.upper()
    key_length = len(key)
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(key[key_index % key_length]) - 65
            encrypted_char = chr((ord(char) - offset + k) % 26 + offset)
            encrypted.append(encrypted_char)
            key_index += 1
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def main():
    input_file = input("Enter the name of the text file to encrypt: ").strip()
    key = input("Enter the Vigenère cipher key (alphabetic): ").strip()
    if not key.isalpha():
        print("Key must contain only alphabetic characters.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        return

    ciphertext = vigenere_encrypt(plaintext, key)
    with open("output.txt", 'w', encoding='utf-8') as f:
        f.write(ciphertext)
    print("Encryption complete! Output saved as 'output.txt'.")

if __name__ == "__main__":
    main()
