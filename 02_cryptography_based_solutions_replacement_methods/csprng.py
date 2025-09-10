import os
import secrets
import datetime

def print_intro():
    """Prints a welcome message and explanation for the students."""
    print("="*70)
    print("🔑 Welcome to the Interactive CSPRNG OTP Encryptor 🔑")
    print("="*70)
    print("\nHello Students! This program will demonstrate the full One-Time Pad process.")
    print("It will also include an optional section showing what happens when a key")
    print("is incorrectly used more than once (a 'Two-Time Pad' attack).\n")
    print("1. You will provide a secret message.")
    print("2. The program will generate a truly random key of the exact same length.")
    print("3. It will perform the encryption and show a step-by-step XOR breakdown.")
    print("4. You will have the option to see a detailed, automated attack on the reused key.\n")
    print("-" * 70)

def get_algorithm_choice():
    """Lets the user choose which Python module to use for generation."""
    print("Python provides two main ways to access the OS's CSPRNG:")
    print("  1. secrets: The modern, recommended module for all cryptographic uses.")
    print("  2. os.urandom: The original, lower-level function that also works perfectly.\n")
    while True:
        choice = input("Which algorithm do you want to use? (Enter 1 or 2): ")
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid input. Please enter 1 or 2.")

def get_user_message(prompt):
    """Gets a secret message from the user with a custom prompt."""
    while True:
        message = input(prompt)
        if message:
            return message
        else:
            print("Message cannot be empty. Please try again.")

def generate_otp_key(length_in_bytes, algorithm):
    """Generates a single OTP key using the chosen algorithm."""
    if algorithm == '1':
        return secrets.token_bytes(length_in_bytes)
    else:
        return os.urandom(length_in_bytes)

def encrypt_message(plaintext_bytes, key_bytes):
    """Encrypts the message by XORing each byte of the plaintext with the key."""
    return bytes([p_byte ^ k_byte for p_byte, k_byte in zip(plaintext_bytes, key_bytes)])

def display_data(title, byte_data):
    """Displays byte data in ASCII, Hexadecimal, and Binary formats."""
    print(f"--- {title} ---")
    ascii_representation = repr(byte_data.decode('latin1'))
    print(f"  - ASCII (Full)   : {ascii_representation}")
    hex_string = byte_data.hex()
    print(f"  - Hexadecimal    : {hex_string}")
    binary_string = ' '.join(f'{byte:08b}' for byte in byte_data)
    print(f"  - Binary         : {binary_string}\n")

def show_xor_step_by_step(plaintext_bytes, key_bytes, ciphertext_bytes):
    """Displays a detailed, character-by-character breakdown of the XOR operation."""
    print("\n" + "="*70)
    print("🔬 Step-by-Step XOR Operation Breakdown 🔬")
    print("="*70)
    print("\nEach character of the plaintext is XORed with the corresponding character of the key.\n")
    print("Plaintext         XOR  Key               =  Ciphertext")
    print("Char | Binary           Char | Binary           Char | Binary")
    print("-----+------------      -----+------------      -----+------------")
    for i in range(len(plaintext_bytes)):
        p_char = repr(chr(plaintext_bytes[i]))[1:-1]
        p_bin = f'{plaintext_bytes[i]:08b}'
        k_char = repr(chr(key_bytes[i]))[1:-1]
        k_bin = f'{key_bytes[i]:08b}'
        c_char = repr(chr(ciphertext_bytes[i]))[1:-1]
        c_bin = f'{ciphertext_bytes[i]:08b}'
        print(f"{p_char:<4} | {p_bin}      {k_char:<4} | {k_bin}      {c_char:<4} | {c_bin}")

def calculate_readability_score(byte_data):
    """Scores text based on how many printable ASCII characters it contains."""
    score = 0
    for byte in byte_data:
        # Check for letters, numbers, punctuation, and space
        if 32 <= byte <= 126:
            score += 1
    return score

def demonstrate_two_time_pad_attack(p1_bytes, c1_bytes, key_bytes):
    """Simulates the catastrophic failure of reusing an OTP key."""
    print("\n" + "="*70)
    print("🚨 Two-Time Pad Attack Demonstration (Project Venona Scenario) 🚨")
    print("="*70)
    print("\nCRITICAL MISTAKE: We are about to use the SAME KEY for a new message.")
    print("An attacker who intercepts both encrypted messages can now break the code.\n")

    p1_len = len(p1_bytes)
    p2_text = get_user_message(f"Enter a second secret message (will be adjusted to length {p1_len}): ")
    if len(p2_text) < p1_len:
        p2_text += ' ' * (p1_len - len(p2_text))
        print(f"INFO: Your message was too short and has been padded with spaces.")
    elif len(p2_text) > p1_len:
        p2_text = p2_text[:p1_len]
        print(f"INFO: Your message was too long and has been truncated.")
    p2_bytes = p2_text.encode('latin1')
    c2_bytes = encrypt_message(p2_bytes, key_bytes)
    
    print("\n--- The Second Encryption ---")
    display_data("Message 2 (Adjusted Plaintext)", p2_bytes)
    display_data("Message 2 (Ciphertext)", c2_bytes)
    
    p1_xor_p2 = encrypt_message(c1_bytes, c2_bytes)
    print("\n--- The Attacker's View ---")
    print("The attacker XORs the two ciphertexts to get (Plaintext 1 ⊕ Plaintext 2).\n")
    display_data("Result of (Ciphertext 1 ⊕ Ciphertext 2)", p1_xor_p2)

    print("\n--- Automated Crib Dragging ---")
    print("The attacker must guess a word (a 'crib') and test it in every position.")
    crib = get_user_message("Enter a word you guess is in one of the messages (the 'crib'): ")
    crib_bytes = crib.encode('latin1')

    print("\nNow dragging the crib across the data. The attempt with the most")
    print("readable text is the most likely breakthrough...\n")
    
    best_score = -1
    best_guess_text = b''
    best_position = -1

    for pos in range(len(p1_bytes) - len(crib_bytes) + 1):
        # Create a full-length byte string with the crib at the current position
        padded_crib = (b'\0' * pos) + crib_bytes
        padded_crib = padded_crib.ljust(len(p1_bytes), b'\0')
        
        revealed_bytes = encrypt_message(p1_xor_p2, padded_crib)
        score = calculate_readability_score(revealed_bytes)
        
        # Display the result of this attempt
        revealed_ascii = repr(revealed_bytes.decode('latin1'))
        print(f"Position {pos:02d}: {revealed_ascii}")

        if score > best_score:
            best_score = score
            best_guess_text = revealed_bytes
            best_position = pos
    
    print("\n" + "-"*70)
    print("🏆 Best Result Found! 🏆")
    print("-"*70)
    print(f"The most readable text was found when the crib '{crib}' was placed at position {best_position}.")
    print("This reveals a piece of the other message:\n")
    display_data("Most Likely Revealed Text", best_guess_text)


def main():
    """Main function to run the program."""
    print_intro()
    algo_choice = get_algorithm_choice()
    message_text = get_user_message("\nEnter the first secret message: ")
    message_bytes = message_text.encode('latin1')
    key_len_bytes = len(message_bytes)
    
    print("\n" + "="*70)
    print("🔒 OTP Encryption Demonstration 🔒")
    print("="*70)
    key_bytes = generate_otp_key(key_len_bytes, algo_choice)
    ciphertext_bytes = encrypt_message(message_bytes, key_bytes)
    display_data("Original Message (Plaintext)", message_bytes)
    display_data("Generated OTP Key", key_bytes)
    display_data("Encrypted Message (Ciphertext)", ciphertext_bytes)
    show_xor_step_by_step(message_bytes, key_bytes, ciphertext_bytes)
    
    print("\n" + "="*70)
    while True:
        choice = input("Would you like to see a demonstration of the two-time pad attack? (yes/no): ").lower()
        if choice in ['yes', 'y']:
            demonstrate_two_time_pad_attack(message_bytes, ciphertext_bytes, key_bytes)
            break
        elif choice in ['no', 'n']:
            break
    
    print("\n" + "="*70)
    print("\n🗓️ Here is your list of UNUSED OTP keys for each hour of tomorrow. 🗓️\n")
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    start_of_tomorrow = datetime.datetime.combine(tomorrow, datetime.time.min)
    for i in range(24):
        key_timestamp = start_of_tomorrow + datetime.timedelta(hours=i)
        formatted_time = key_timestamp.strftime("%Y-%m-%d %H:00")
        scheduled_key_bytes = generate_otp_key(key_len_bytes, algo_choice)
        print(f"--- Key for {formatted_time} ---")
        display_data(f"Scheduled Key", scheduled_key_bytes)

if __name__ == "__main__":
    main()