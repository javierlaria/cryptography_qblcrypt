import string

def welcome():
    """Prints the welcome message and explanation of the cipher."""
    print("=" * 60)
    print("🛤️  RAIL FENCE (ZIG-ZAG) CIPHER DEMO — by Pedro V")
    print("=" * 60)
    print("\n📖 Welcome! This tool demonstrates the Rail Fence cipher, a classic")
    print("   example of a 'transposition' cipher.")
    print("\nIn other words, the letters of the message are not changed,")
    print("they are simply rearranged in a different order.")
    print("-" * 60)
    print("💡 Core idea: The message is written in a zig-zag pattern across")
    print("   a number of 'rails' (rows). The ciphertext is then read")
    print("   off rail by rail.")
    print("\n   Plaintext:  WE ARE DISCOVERED FLEE AT ONCE")
    print("   Key (Rails): 3")
    print("\n   W . . . E . . . C . . . R . . . L . . . T . . . E")
    print("   . E . R . D . S . O . E . E . F . E . A . O . C .")
    print("   . . A . . . I . . . V . . . D . . . E . . . N . .")
    print("\n   Ciphertext: WECRLTEERDSOEEFEAOCAIVDEN")
    print("-" * 60)
    print("⚠️  This cipher is not secure! The key (number of rails) is")
    print("    usually a small number and can be easily brute-forced.")
    print("    Its purpose here is purely educational.\n")

def get_rails(prompt="🔑 Enter the number of rails (the key, must be > 1): "):
    """Gets and validates the number of rails from the user."""
    while True:
        try:
            rails = int(input(prompt))
            if rails > 1:
                return rails
            else:
                print("Error: Number of rails must be greater than 1.")
        except ValueError:
            print("Error: Please enter a valid integer.")

def print_fence(fence):
    """Prints a visual representation of the fence."""
    print("\nVisualizing the 'fence' pattern:")
    for rail in fence:
        print("".join(rail))

def encrypt(plaintext, rails):
    """Encrypts a message using the Rail Fence cipher."""
    if rails <= 1:
        return plaintext

    fence = [[' ' for _ in range(len(plaintext))] for _ in range(rails)]
    
    rail = 0
    direction = 1

    for i, char in enumerate(plaintext):
        fence[rail][i] = char
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
        
    print_fence(fence)
    
    ciphertext = "".join(char for r in fence for char in r if char != ' ')
    return ciphertext

def decrypt(ciphertext, rails):
    """Decrypts a message from the Rail Fence cipher."""
    if rails <= 1:
        return ciphertext

    fence = [[' ' for _ in range(len(ciphertext))] for _ in range(rails)]
    
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        fence[rail][i] = '?'
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    cipher_index = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if fence[r][c] == '?' and cipher_index < len(ciphertext):
                fence[r][c] = ciphertext[cipher_index]
                cipher_index += 1
    
    plaintext = ""
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        plaintext += fence[rail][i]
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
        
    return plaintext

def run_encrypt_mode():
    """Runs the encryption part of the demo."""
    print("\n--- Encrypt Mode ---")
    message = input("✉️  Enter your message to encrypt: ").upper()
    cleaned_message = ''.join([c for c in message if c in string.ascii_uppercase])
    
    if not cleaned_message:
        print("No valid message entered.")
        return
        
    print(f"\n✅ Cleaned Message: {cleaned_message}")
    rails = get_rails()
    
    print("\nEncrypting your message...")
    ciphertext = encrypt(cleaned_message, rails)
    print(f"\n🔒 Encrypted Ciphertext: {ciphertext}")

def run_decrypt_mode():
    """Runs the decryption part of the demo."""
    print("\n--- Decrypt Mode ---")
    message = input("✉️  Enter the ciphertext to decrypt: ").upper()
    cleaned_message = ''.join([c for c in message if c in string.ascii_uppercase])

    if not cleaned_message:
        print("No valid ciphertext entered.")
        return

    rails = get_rails()
    decrypted_message = decrypt(cleaned_message, rails)
    print(f"\n🔓 Decrypted Plaintext: {decrypted_message}")

def run_brute_force_mode():
    """Runs the brute-force attack demo."""
    print("\n--- Brute-Force Attack Mode ---")
    message = input("✉️  Enter the ciphertext to attack: ").upper()
    cleaned_message = ''.join([c for c in message if c in string.ascii_uppercase])

    if not cleaned_message:
        print("No valid ciphertext entered.")
        return

    max_rails = get_rails("Enter the maximum number of rails to try (e.g., 10): ")

    print(f"\n⚔️  Brute-forcing ciphertext '{cleaned_message}' with keys 2 to {max_rails}...")
    print("-" * 60)
    for key_attempt in range(2, max_rails + 1):
        possible_plaintext = decrypt(cleaned_message, key_attempt)
        print(f"Key = {key_attempt:2d}: {possible_plaintext}")
    print("-" * 60)
    print("\nLook through the list above. Can you spot a meaningful message?")

def main():
    """Main function to run the demonstration with a menu."""
    welcome()
    
    while True:
        print("\n" + "="*25 + " MENU " + "="*27)
        print("1. Encrypt a message")
        print("2. Decrypt a message with a known key")
        print("3. Brute-force a ciphertext")
        print("4. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            run_encrypt_mode()
        elif choice == '2':
            run_decrypt_mode()
        elif choice == '3':
            run_brute_force_mode()
        elif choice == '4':
            print("\nHappy ciphering! Exiting the demo.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
