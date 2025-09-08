#
# 🔐 Advanced Demo: XOR Cipher Scenarios (Student-Friendly Version)
# Purpose: To demonstrate XOR encryption with clear, step-by-step conversions
#          and a corrected, more intuitive reused key attack demo.
#

import random
import time

# --- Core Helper Functions ---

def text_to_binary(text):
    """Converts a string of text into a single string of binary."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    """Converts a string of binary back into human-readable text."""
    if len(binary_string) % 8 != 0:
        return "[Error: Invalid binary length]"
    try:
        chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
        return ''.join(chars)
    except (ValueError, TypeError):
        return "[Unprintable Characters]"

def generate_binary_key(length):
    """Generates a truly random binary key of a specific length."""
    return ''.join(random.choice(['0', '1']) for _ in range(length))

def xor_cipher(binary_message, binary_key):
    """Performs the XOR operation between two binary strings."""
    return ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary_message, binary_key))

def repeat_key_to_length(binary_key, target_length):
    """Repeats a short binary key until it matches the target length."""
    return (binary_key * (target_length // len(binary_key) + 1))[:target_length]

def pause_and_explain(message):
    """A helper function to print a message and wait for user input."""
    print(f"\n▶️ {message}")
    input("  Press Enter to continue...")

def display_text_to_binary_conversion(text, title="Text to Binary Conversion"):
    """Shows the step-by-step conversion of text to binary for students."""
    print(f"\n--- {title} ---")
    for char in text[:5]: # Show conversion for the first 5 chars to keep it brief
        print(f"  Character '{char}' -> ASCII {ord(char):<3} -> Binary '{format(ord(char), '08b')}'")
    if len(text) > 5:
        print("  ...")
    print("-" * (len(title) + 6))

# --- Demonstration Scenarios ---

def demo_repeating_key():
    """Demonstrates a Vigenère-style cipher using a short, repeating XOR key."""
    print("\n" + "="*60)
    print("DEMO 1: The Weakness of a Short, Repeating Key")
    print("="*60)
    
    message = input("✉️ Enter a message (e.g., 'THE EAGLE HAS LANDED'): ").upper()
    short_key = input("🔑 Enter a SHORT key (e.g., 'KEY'): ").upper()

    display_text_to_binary_conversion(message, "Step 1: Convert Message to Binary")
    message_bin = text_to_binary(message)
    
    display_text_to_binary_conversion(short_key, "Step 2: Convert Key to Binary")
    short_key_bin = text_to_binary(short_key)

    pause_and_explain(f"Our message has {len(message_bin)} bits, but our key only has {len(short_key_bin)} bits. We must repeat the key to match the message length.")
    
    repeated_key_bin = repeat_key_to_length(short_key_bin, len(message_bin))
    
    print("\n--- Step 3: Repeating the Key ---")
    print(f"Message Binary : {message_bin[:80]}...")
    print(f"Repeated Key   : {repeated_key_bin[:80]}...")
    print("\nNotice the repeating pattern in the key. This pattern can be analyzed by attackers to break the code!")
    
    pause_and_explain("Now, let's encrypt the message using this predictable, repeating key.")
    
    ciphertext_bin = xor_cipher(message_bin, repeated_key_bin)
    print("\n--- Step 4: Encryption Result ---")
    print(f"Ciphertext (Binary): {ciphertext_bin[:80]}...")
    print(f"Ciphertext (Text)  : {repr(binary_to_text(ciphertext_bin))}")
    print("\nBecause the key is patterned, the ciphertext also contains subtle patterns. This is NOT secure.")

def demo_one_time_pad():
    """Demonstrates a proper One-Time Pad with a long, random key."""
    print("\n" + "="*60)
    print("DEMO 2: The One-Time Pad (Perfect Secrecy)")
    print("="*60)
    
    message = input("✉️ Enter a message (e.g., 'ATTACK AT DAWN'): ").upper()
    
    display_text_to_binary_conversion(message, "Step 1: Convert Message to Binary")
    message_bin = text_to_binary(message)
    
    pause_and_explain("For a true One-Time Pad, the key must be random and exactly as long as the message.")
    
    key_bin = generate_binary_key(len(message_bin))
    print("\n--- Step 2: Generating a Secure Key ---")
    print(f"Random Key    : {key_bin[:80]}...")
    print("This key is completely random and has no pattern.")

    pause_and_explain("Let's encrypt with this secure key.")
    
    ciphertext_bin = xor_cipher(message_bin, key_bin)
    print("\n--- Step 3: Encryption Result ---")
    print(f"Ciphertext (Binary): {ciphertext_bin[:80]}...")
    print(f"Ciphertext (Text)  : {repr(binary_to_text(ciphertext_bin))}")

    pause_and_explain("To decrypt, the receiver uses the exact same key.")
    
    decrypted_bin = xor_cipher(ciphertext_bin, key_bin)
    decrypted_text = binary_to_text(decrypted_bin)
    print("\n--- Step 4: Decryption Result ---")
    print(f"Decrypted (Binary): {decrypted_bin[:80]}...")
    print(f"Decrypted (Text)  : {decrypted_text}")
    print("\nSuccess! We recovered the original message.")

def demo_reused_key_attack():
    """Demonstrates the catastrophic failure when an OTP key is used twice."""
    print("\n" + "="*60)
    print("DEMO 3: The Reused Key Attack (NEVER do this!)")
    print("="*60)
    
    message1 = input("✉️ Enter the first secret message: ").upper()
    message2 = input("✉️ Enter the second secret message: ").upper()
    
    min_len = min(len(message1), len(message2))
    message1, message2 = message1[:min_len], message2[:min_len]
    print(f"\n(Messages will be compared up to the shortest length: {min_len} characters)")
    print(f"  Message 1: '{message1}'")
    print(f"  Message 2: '{message2}'")

    display_text_to_binary_conversion(message1, "Step 1: Convert Message 1 to Binary")
    m1_bin = text_to_binary(message1)
    
    display_text_to_binary_conversion(message2, "Step 2: Convert Message 2 to Binary")
    m2_bin = text_to_binary(message2)

    pause_and_explain("Let's generate a single One-Time Pad key.")
    key_bin = generate_binary_key(len(m1_bin))
    print(f"The Secret Key: {key_bin[:80]}...")

    pause_and_explain("Now, we encrypt the FIRST message with this key. This is secure so far.")
    c1_bin = xor_cipher(m1_bin, key_bin)
    print(f"Ciphertext 1: {repr(binary_to_text(c1_bin))}")

    pause_and_explain("CRITICAL MISTAKE: Now, we encrypt the SECOND message with the SAME key.")
    c2_bin = xor_cipher(m2_bin, key_bin)
    print(f"Ciphertext 2: {repr(binary_to_text(c2_bin))}")

    pause_and_explain("An attacker intercepts both ciphertexts. They can now XOR them together to eliminate the key.")
    
    print("\n--- The Attack ---")
    print("Math: C1 ⊕ C2 = (M1 ⊕ K) ⊕ (M2 ⊕ K)")
    print("The keys cancel out: K ⊕ K = 0, so... C1 ⊕ C2 = M1 ⊕ M2")
    
    attack_result_bin = xor_cipher(c1_bin, c2_bin)
    attack_result_text = binary_to_text(attack_result_bin)
    print(f"\nAttacker's Result (M1 ⊕ M2): {repr(attack_result_text)}")
    print("The key is gone! This result is the XOR of the two original plaintexts.")

    pause_and_explain("This result leaks info. Let's demonstrate with a 'crib drag'. An attacker guesses a likely word in one message to reveal the other.")
    
    crib = input(f"Enter a word you GUESS is in Message 1 or 2 (e.g., 'SECRET' or 'LAUNCH'): ").upper()
    
    start_index = -1
    crib_in_m1 = False
    if crib in message1:
        start_index = message1.find(crib)
        crib_in_m1 = True
    elif crib in message2:
        start_index = message2.find(crib)
    
    if start_index != -1:
        print(f"\nCorrect guess! '{crib}' was found.")
        pause_and_explain("Now we will perform the final step of the attack, character by character.")
        
        # --- NEW: DETAILED REVEAL SECTION ---
        print("\n" + "-"*60)
        print("--- The 'Aha!' Moment: Revealing the Secret Bit-by-Bit ---")
        print("Logic: (M1 ⊕ M2) ⊕ Guessed_Part_of_M2 = Revealed_Part_of_M1")
        print("-"*60)
        
        revealed_text = ""
        for i in range(len(crib)):
            # Get the relevant characters for this step
            guessed_char = crib[i]
            result_char = attack_result_text[start_index + i]
            
            # Convert to binary to show the operation
            guessed_char_bin = text_to_binary(guessed_char)
            result_char_bin = text_to_binary(result_char)
            
            # Perform the XOR to find the revealed character's binary
            revealed_char_bin = xor_cipher(result_char_bin, guessed_char_bin)
            revealed_char = binary_to_text(revealed_char_bin)
            revealed_text += revealed_char

            print(f"\nStep {i+1}: Revealing character at position {start_index + i}")
            if crib_in_m1:
                print(f"  We guessed '{guessed_char}' is in Message 1. This reveals Message 2.")
                other_message_char = message2[start_index + i]
            else:
                print(f"  We guessed '{guessed_char}' is in Message 2. This reveals Message 1.")
                other_message_char = message1[start_index + i]
            
            print("  ------------------------------------------------")
            print(f"  Attacker's Result ('{result_char}') : {result_char_bin}")
            print(f"  XOR with Guess    ('{guessed_char}') : {guessed_char_bin}")
            print("  ================================================")
            print(f"  Revealed Binary             : {revealed_char_bin}")
            print(f"  Which is the character...   : '{revealed_char}'")
            print("  ------------------------------------------------")
            
            # Verify for the students
            assert revealed_char == other_message_char
            time.sleep(1.5) # Pause to let the information sink in
            
        print("\n✅ Attack successful!")
        if crib_in_m1:
            print(f"By guessing '{crib}' was in Message 1, we fully revealed '{revealed_text}' from Message 2.")
        else:
             print(f"By guessing '{crib}' was in Message 2, we fully revealed '{revealed_text}' from Message 1.")

    else:
        print(f"\nSorry, the word '{crib}' wasn't found in either message. The attack relies on a correct guess.")

# --- Main Program Loop ---

def main():
    """Main function to display the menu and run the demos."""
    while True:
        print("\n" + "#"*60)
        print("##            XOR Cipher Demonstration Tool           ##")
        print("#"*60)
        print("1. Demo a Weak Repeating-Key Cipher (Vigenère)")
        print("2. Demo a Secure One-Time Pad")
        print("3. Demo the Reused Key Attack")
        print("4. Exit")
        
        choice = input("Select a demo to run [1-4]: ")
        
        if choice == '1':
            demo_repeating_key()
        elif choice == '2':
            demo_one_time_pad()
        elif choice == '3':
            demo_reused_key_attack()
        elif choice == '4':
            print("Exiting demo. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
        
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
