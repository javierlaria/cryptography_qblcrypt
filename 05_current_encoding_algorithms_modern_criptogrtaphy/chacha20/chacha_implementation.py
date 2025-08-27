# ChaCha20 implementation using the 'cryptography' library
# Installation: pip install cryptography
# This is a standalone script using a dedicated library for efficiency and security.
# Students: Use this as a reference. For the same key, nonce, and plaintext, you should get identical ciphertext.
# Note: This uses the IETF ChaCha20 (RFC 8439) via the library.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def chacha20_encrypt(key, nonce_12, plaintext, initial_counter=0):
    """Encrypt (or decrypt) plaintext using ChaCha20. Returns ciphertext as bytes."""
    # The library requires a 16-byte nonce: 4-byte initial counter + 12-byte nonce
    full_nonce = initial_counter.to_bytes(4, 'little') + nonce_12
    
    # Create the ChaCha20 algorithm instance
    algorithm = algorithms.ChaCha20(key, full_nonce)
    
    # Create the cipher object (stream cipher, no mode needed)
    cipher = Cipher(algorithm, mode=None)
    
    # Encryptor (same for decryption since it's XOR-based)
    encryptor = cipher.encryptor()
    
    # Encrypt the entire plaintext in one go (library handles streaming internally)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return ciphertext

# For classroom use: Fixed key and nonce so all students get the same output for the same plaintext
FIXED_KEY = bytes.fromhex('00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f')  # 32 bytes
FIXED_NONCE = bytes.fromhex('00 00 00 00 00 00 00 00 00 00 00 00')  # 12 bytes (96-bit)

if __name__ == "__main__":
    # Prompt for custom plaintext input
    plaintext_str = input("Enter your plaintext message: ")
    plaintext = plaintext_str.encode('utf-8')  # Convert string to bytes
    
    # Encrypt using fixed key and nonce (initial counter=0 to match pure Python version)
    ciphertext = chacha20_encrypt(FIXED_KEY, FIXED_NONCE, plaintext, initial_counter=0)
    
    # Output the ciphertext in hex for easy comparison
    print("Ciphertext (hex):", ciphertext.hex())
    
    # Optional: Decrypt to verify (should match original plaintext)
    decrypted = chacha20_encrypt(FIXED_KEY, FIXED_NONCE, ciphertext, initial_counter=0)
    print("Decrypted (verification):", decrypted.decode('utf-8'))
