import struct
import numpy as np

def ROTL32(x, n):
    """Rotate left a 32-bit word by n bits"""
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def quarter_round(a, b, c, d):
    """
    Perform a ChaCha20 quarter round operation on four 32-bit words.
    
    Args:
        a, b, c, d: Four 32-bit words to process
        
    Returns:
        The modified a, b, c, d after the quarter round
    """
    # Step 1: Addition, XOR, and Rotate Left (16 bits)
    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = ROTL32(d, 16)
    
    # Step 2: Addition, XOR, and Rotate Left (12 bits)
    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = ROTL32(b, 12)
    
    # Step 3: Addition, XOR, and Rotate Left (8 bits)
    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = ROTL32(d, 8)
    
    # Step 4: Addition, XOR, and Rotate Left (7 bits)
    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = ROTL32(b, 7)
    
    return a, b, c, d

def print_state(step_name, state, indices=None):
    """
    Print the state matrix in a readable format with explanations.
    
    Args:
        step_name: Description of what step we're showing
        state: The 4x4 state matrix
        indices: Optional indices to highlight specific elements
    """
    print(f"\n--- {step_name} ---")
    for i in range(4):
        row = []
        for j in range(4):
            val = f"{state[i*4+j]:08x}"
            if indices and (i*4+j) in indices:
                val = f"[{val}]"  # Highlight specific indices
            row.append(val)
        print(" ".join(row))

def chacha20_block(key, counter, nonce, rounds=20):
    """
    Generate a single 64-byte ChaCha20 keystream block.
    
    Args:
        key: 32-byte key (as bytes)
        counter: 32-bit block counter
        nonce: 12-byte nonce (as bytes)
        rounds: Number of rounds (default 20 for ChaCha20)
        
    Returns:
        64-byte keystream block
    """
    # Constants for ChaCha20
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    # Convert key to list of 32-bit words (little-endian)
    key_words = list(struct.unpack('<8L', key))
    
    # Convert nonce to list of 32-bit words (little-endian)
    nonce_words = list(struct.unpack('<3L', nonce))
    
    # Step 1: Form the initial state matrix (4x4 of 32-bit words)
    # Layout: [constants][key][counter][nonce]
    state = [
        constants[0], constants[1], constants[2], constants[3],
        key_words[0], key_words[1], key_words[2], key_words[3],
        key_words[4], key_words[5], key_words[6], key_words[7],
        counter, nonce_words[0], nonce_words[1], nonce_words[2]
    ]
    
    print_state("Initial State", state)
    print("Layout: [constants][key][counter][nonce]")
    
    # Step 2: Make a working copy of the state
    working_state = state.copy()
    print("\nMade a working copy of the state for mixing")
    
    # Step 3: Perform the core rounds (20 rounds total)
    for round_idx in range(rounds // 2):
        # Column rounds (even rounds)
        print(f"\n--- Column Round {round_idx*2} ---")
        
        # Apply quarter-round to each column
        for col in range(4):
            indices = [col, col+4, col+8, col+12]
            print(f"Column {col}: indices {indices}")
            
            # Get the values for this column
            a, b, c, d = [working_state[i] for i in indices]
            
            # Apply quarter round
            a, b, c, d = quarter_round(a, b, c, d)
            
            # Store back the results
            working_state[col] = a
            working_state[col+4] = b
            working_state[col+8] = c
            working_state[col+12] = d
            
            print_state(f"After column {col} quarter-round", working_state, indices)
        
        # Diagonal rounds (odd rounds)
        print(f"\n--- Diagonal Round {round_idx*2+1} ---")
        
        # Apply quarter-round to each diagonal
        diagonals = [
            [0, 5, 10, 15],  # Main diagonal
            [1, 6, 11, 12],  # Diagonal 1
            [2, 7, 8, 13],   # Diagonal 2
            [3, 4, 9, 14]    # Diagonal 3
        ]
        
        for diag_idx, indices in enumerate(diagonals):
            print(f"Diagonal {diag_idx}: indices {indices}")
            
            # Get the values for this diagonal
            a, b, c, d = [working_state[i] for i in indices]
            
            # Apply quarter round
            a, b, c, d = quarter_round(a, b, c, d)
            
            # Store back the results
            for i, val in zip(indices, [a, b, c, d]):
                working_state[i] = val
            
            print_state(f"After diagonal {diag_idx} quarter-round", working_state, indices)
    
    # Step 4: Add the original state to the working state
    print("\n--- Final Addition ---")
    print("Adding original state to mixed state (mod 2^32)")
    
    for i in range(16):
        working_state[i] = (working_state[i] + state[i]) & 0xFFFFFFFF
    
    print_state("Final State After Addition", working_state)
    
    # Step 5: Serialize the state to a 64-byte keystream block
    print("\n--- Serialization ---")
    print("Converting state to little-endian byte sequence")
    
    keystream = b''
    for word in working_state:
        keystream += struct.pack('<L', word)
    
    print(f"Keystream (first 16 bytes): {keystream[:16].hex()}")
    return keystream

def chacha20_encrypt(key, nonce, plaintext, counter=0):
    """
    Encrypt plaintext using ChaCha20.
    
    Args:
        key: 32-byte encryption key
        nonce: 12-byte nonce
        plaintext: Message to encrypt
        counter: Starting block counter (default 0)
        
    Returns:
        ciphertext: Encrypted message
    """
    ciphertext = b''
    
    # Process the plaintext in 64-byte blocks
    for i in range(0, len(plaintext), 64):
        # Generate keystream block for current counter
        print(f"\n{'='*60}")
        print(f"Processing block {counter} (bytes {i}-{min(i+63, len(plaintext)-1)})")
        print(f"{'='*60}")
        
        keystream_block = chacha20_block(key, counter, nonce)
        
        # Get the current plaintext block
        block = plaintext[i:i+64]
        
        # XOR plaintext with keystream
        encrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
        
        # Add to ciphertext
        ciphertext += encrypted_block
        
        # Increment counter for next block
        counter += 1
    
    return ciphertext

# For classroom demonstration
if __name__ == "__main__":
    print("ChaCha20 Educational Implementation")
    print("===================================\n")
    
    # Fixed key and nonce for reproducible results
    KEY = bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')
    NONCE = bytes.fromhex('000000000000004a00000000')
    
    print(f"Key: {KEY.hex()}")
    print(f"Nonce: {NONCE.hex()}")
    
    # Get input from user
    plaintext = input("\nEnter message to encrypt: ").encode('utf-8')
    
    print(f"\nPlaintext: {plaintext.hex()}")
    print(f"Length: {len(plaintext)} bytes")
    
    # Encrypt the message
    ciphertext = chacha20_encrypt(KEY, NONCE, plaintext)
    
    print(f"\nFinal Ciphertext: {ciphertext.hex()}")
    
    # Decryption is the same process
    decrypted = chacha20_encrypt(KEY, NONCE, ciphertext)
    print(f"\nDecrypted: {decrypted.decode('utf-8')}")
    
    # Verify encryption/decryption worked
    if decrypted == plaintext:
        print("\n✓ Encryption/Decryption successful!")
    else:
        print("\n✗ Encryption/Decryption failed!")
