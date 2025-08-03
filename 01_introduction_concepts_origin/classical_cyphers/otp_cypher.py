import random
import string
from itertools import product

# Minimal English words for demo (expand as needed)
ENGLISH_WORDS = {
    "HI", "ME", "AT", "IN", "THE", "AND", "YOU", "WE", "HE", "SHE", "IT", "ON", "BY", "OR", "IF", "NO", "YES"
}

def welcome():
    print("=" * 60)
    print("🔐 ONE-TIME PAD DEMO — by Pedro V.")
    print("=" * 60)
    print("\n📖 Welcome! This tool demonstrates Claude Shannon's principle of")
    print("    🔒 Perfect Secrecy: P(M | C) = P(M)")
    print("\nIn other words, the ciphertext gives absolutely no clue about")
    print("the original message. We'll use a real One-Time Pad to show why.")
    print("-" * 60)
    print("💡 Core idea: Encryption uses modular addition with a truly random key")
    print("   - Each letter is turned into a number (A=0, ..., Z=25)")
    print("   - Encrypted letter = (Plaintext + Key) mod 26")
    print("   - Decryption = (Ciphertext - Key) mod 26")
    print("-" * 60)
    print("⚠️ OTP is perfectly secure *only if*:")
    print("   1. Key is truly random")
    print("   2. Key is as long as the message")
    print("   3. Key is used ONLY ONCE")
    print("   4. Key is kept secret")
    print("That's why OTP is secure but impractical for modern communication.\n")

def generate_key(length):
    return [random.randint(0, 25) for _ in range(length)]

def encrypt(message, key):
    message_nums = [ord(c) - ord('A') for c in message]
    cipher_nums = [(m + k) % 26 for m, k in zip(message_nums, key)]
    ciphertext = ''.join(chr(c + ord('A')) for c in cipher_nums)
    
    # Step-by-step printout:
    print("\nStep-by-step encryption:")
    print("Char:  ", '  '.join(message))
    print("Index: ", ' '.join(f"{num:2d}" for num in message_nums), "← (A=0)")
    print("Key:   ", ' '.join(f"{k:2d}" for k in key))
    print("-------" + "---" * len(message))
    print("Cipher:", '  '.join(ciphertext))
    return ciphertext

def decrypt(ciphertext, key):
    cipher_nums = [ord(c) - ord('A') for c in ciphertext]
    message_nums = [(c - k) % 26 for c, k in zip(cipher_nums, key)]
    return ''.join(chr(m + ord('A')) for m in message_nums)

def show_possible_plaintexts(ciphertext, trials=5):
    print(f"\n🎭 Showing {trials} equally likely plaintexts for ciphertext: {ciphertext}")
    for _ in range(trials):
        fake_key = generate_key(len(ciphertext))
        possible_plain = decrypt(ciphertext, fake_key)
        print(f"• {possible_plain}  ← possible plaintext (key: {fake_key})")

def brute_force_demo(ciphertext, attempts=10):
    print("\n⚔️ Brute Force Demo: Trying random keys to decrypt ciphertext...")
    print("Notice that *every* random key produces a plausible plaintext.\n")
    for i in range(attempts):
        trial_key = generate_key(len(ciphertext))
        trial_plain = decrypt(ciphertext, trial_key)
        print(f"Attempt {i+1}: {trial_plain}  (Key: {trial_key})")
    print("\n❗ Notice: Without the correct key, you cannot tell which plaintext is real.")

def num_to_char(n):
    return chr(n + ord('A'))

def char_to_num(c):
    return ord(c) - ord('A')

def decrypt_with_key(ciphertext, key):
    cipher_nums = [char_to_num(c) for c in ciphertext]
    message_nums = [(c - k) % 26 for c, k in zip(cipher_nums, key)]
    return ''.join(num_to_char(m) for m in message_nums)

def true_brute_force(ciphertext):
    length = len(ciphertext)
    if length > 4:
        print("\n❌ Message too long for exhaustive brute force (limit 4).")
        return

    total_keys = 26 ** length
    print(f"\n🔍 Performing exhaustive brute force for all {total_keys} keys...")

    candidates = set()
    for key_tuple in product(range(26), repeat=length):
        plaintext = decrypt_with_key(ciphertext, key_tuple)
        if plaintext in ENGLISH_WORDS:
            candidates.add((plaintext, key_tuple))

    if candidates:
        print(f"\n✅ Possible meaningful plaintexts found ({len(candidates)}):")
        for pt, key in sorted(candidates):
            print(f"• {pt} (Key: {list(key)})")
    else:
        print("\n⚠️ No meaningful plaintext found in dictionary for this ciphertext.")

def input_key(length):
    print(f"\nEnter the key for decryption as {length} numbers (0-25) separated by spaces:")
    while True:
        key_str = input("Key: ").strip()
        parts = key_str.split()
        if len(parts) != length:
            print(f"Error: You must enter exactly {length} numbers.")
            continue
        try:
            key = [int(p) for p in parts]
        except ValueError:
            print("Error: Please enter valid integers only.")
            continue
        if any(k < 0 or k > 25 for k in key):
            print("Error: All numbers must be between 0 and 25 inclusive.")
            continue
        return key

def decrypt_another_message():
    print("\n🗝️ Decrypt Another Message Mode")
    ciphertext = input("Enter the ciphertext (letters only): ").upper()
    ciphertext = ''.join([c for c in ciphertext if c in string.ascii_uppercase])
    if not ciphertext:
        print("No valid ciphertext entered.")
        return
    key = input_key(len(ciphertext))
    plaintext = decrypt(ciphertext, key)
    print(f"\n🔓 Decrypted plaintext: {plaintext}")

def main():
    welcome()
    message = input("✉️  Enter your message (letters only, max ~15 chars): ").upper()
    message = ''.join([c for c in message if c in string.ascii_uppercase])
    print(f"\n✅ Cleaned Message: {message}")

    key = generate_key(len(message))
    print(f"\n🗝️  Random One-Time Pad Key: {key}")

    ciphertext = encrypt(message, key)
    print(f"\n🔒 Encrypted Ciphertext: {ciphertext}")

    decrypted = decrypt(ciphertext, key)
    print(f"🔓 Decrypted (with correct key): {decrypted}")

    show_possible_plaintexts(ciphertext)

    choice = input("\nWould you like to see a brute-force demo? (y/n): ").strip().lower()
    if choice == 'y':
        brute_force_demo(ciphertext, attempts=10)

    choice2 = input("\nWould you like to perform exhaustive brute force? (only for messages ≤4 letters) (y/n): ").strip().lower()
    if choice2 == 'y':
        true_brute_force(ciphertext)

    choice3 = input("\nWould you like to decrypt another message? (y/n): ").strip().lower()
    if choice3 == 'y':
        decrypt_another_message()

    print("\n✅ End of demo. You’ve just witnessed Shannon’s Perfect Secrecy in action!")

if __name__ == "__main__":
    main()
