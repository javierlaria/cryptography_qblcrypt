def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Explain the Caesar cipher
print("=== Caesar Cipher Explanation ===")
print("The Caesar cipher is a classical encryption technique where each letter in the text is shifted by a fixed number of positions in the alphabet.")
print("For example, with a shift of 3 (original Caesars), 'A' becomes 'D', 'B' becomes 'E', and so on. Non-alphabetic characters (like spaces or punctuation) remain unchanged.")
print("Encryption shifts letters forward, while decryption shifts them backward by the same amount.")
print("The shift value (1-25) determines how many positions each letter moves. For example, with shift=3, 'Hello' becomes 'Khoor'.")
print("================================")

# Prompt user for action
action = input("Do you want to (E)ncrypt or (D)ecrypt? Enter 'E' or 'D': ").strip().upper()
if action not in ['E', 'D']:
    print("Error: Please enter 'E' for encrypt or 'D' for decrypt.")
    exit(1)

# Get user input for text and shift
text = input("Enter the text to process: ")
try:
    shift = int(input("Enter the shift value (1-25): "))
    if shift < 1 or shift > 25:
        raise ValueError("Shift must be between 1 and 25.")
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# Process the text based on user choice
if action == 'E':
    print(f"\nEncrypting '{text}' with a shift of {shift}...")
    result = caesar_encrypt(text, shift)
    print(f"Each letter is shifted forward by {shift} positions in the alphabet.")
    print(f"For example, 'A' becomes '{chr((ord('A') - ord('A') + shift) % 26 + ord('A'))}' and 'a' becomes '{chr((ord('a') - ord('a') + shift) % 26 + ord('a'))}'.")
    output_description = "Encrypted"
else:
    print(f"\nDecrypting '{text}' with a shift of {shift}...")
    result = caesar_decrypt(text, shift)
    print(f"Each letter is shifted backward by {shift} positions in the alphabet.")
    print(f"For example, 'D' becomes '{chr((ord('D') - ord('A') - shift) % 26 + ord('A'))}' and 'd' becomes '{chr((ord('d') - ord('a') - shift) % 26 + ord('a'))}'.")
    output_description = "Decrypted"

# Save result to file
try:
    with open("caesars_encrypt.txt", "w") as file:
        file.write(result)
    print(f"{output_description} text saved to caesars_encrypt.txt: {result}")
except IOError:
    print("Error: Could not write to file.")

# Display result and verification
print(f"{output_description} result: {result}")
if action == 'E':
    print(f"Verification (decrypting back): {caesar_decrypt(result, shift)}")
else:
    print(f"Verification (encrypting back): {caesar_encrypt(result, shift)}")
