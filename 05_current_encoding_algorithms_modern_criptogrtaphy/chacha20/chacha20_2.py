#!/usr/bin/env python3
"""
ChaCha20 Educational Tool
Combines a functional demonstration with a step-by-step visualizer
to explain the inner workings of the ChaCha20 stream cipher.
"""

import os
import struct
import time
from typing import List, Tuple

# --- ANSI Color Codes for Better Visualization ---
class Colors:
    """Class to hold ANSI color codes for terminal output."""
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"

# ==============================================================================
# === ChaCha20 Core Algorithm Functions
# ==============================================================================

def rotl32(x: int, n: int) -> int:
    """
    Performs a 32-bit left rotation.
    Example: rotl32(0x12345678, 8) -> 0x34567812
    """
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def quarter_round(a: int, b: int, c: int, d: int) -> Tuple[int, int, int, int]:
    """
    Executes the ChaCha20 quarter round function on four 32-bit integers.
    This is the core mixing operation of the algorithm.
    """
    a = (a + b) & 0xffffffff; d ^= a; d = rotl32(d, 16)
    c = (c + d) & 0xffffffff; b ^= c; b = rotl32(b, 12)
    a = (a + b) & 0xffffffff; d ^= a; d = rotl32(d, 8)
    c = (c + d) & 0xffffffff; b ^= c; b = rotl32(b, 7)
    return a, b, c, d

def chacha20_block_generator(key: bytes, counter: int, nonce: bytes) -> bytes:
    """
    Generates one 64-byte ChaCha20 keystream block.

    Args:
        key: The 32-byte (256-bit) secret key.
        counter: The 4-byte block counter.
        nonce: The 12-byte (96-bit) number used once.

    Returns:
        A 64-byte block of pseudorandom keystream data.
    """
    # ChaCha20 constants "expand 32-byte k"
    constants = (0x61707865, 0x3320646e, 0x79622d32, 0x6b206574)

    # The initial state is a 4x4 matrix of 32-bit words.
    state = list(constants +
                 struct.unpack("<8I", key) +
                 (counter,) +
                 struct.unpack("<3I", nonce))

    working_state = state[:]

    # 10 rounds of mixing (each round consists of a column and diagonal round)
    for _ in range(10):
        # Column rounds
        working_state[0], working_state[4], working_state[8],  working_state[12] = quarter_round(working_state[0], working_state[4], working_state[8],  working_state[12])
        working_state[1], working_state[5], working_state[9],  working_state[13] = quarter_round(working_state[1], working_state[5], working_state[9],  working_state[13])
        working_state[2], working_state[6], working_state[10], working_state[14] = quarter_round(working_state[2], working_state[6], working_state[10], working_state[14])
        working_state[3], working_state[7], working_state[11], working_state[15] = quarter_round(working_state[3], working_state[7], working_state[11], working_state[15])
        # Diagonal rounds
        working_state[0], working_state[5], working_state[10], working_state[15] = quarter_round(working_state[0], working_state[5], working_state[10], working_state[15])
        working_state[1], working_state[6], working_state[11], working_state[12] = quarter_round(working_state[1], working_state[6], working_state[11], working_state[12])
        working_state[2], working_state[7], working_state[8],  working_state[13] = quarter_round(working_state[2], working_state[7], working_state[8],  working_state[13])
        working_state[3], working_state[4], working_state[9],  working_state[14] = quarter_round(working_state[3], working_state[4], working_state[9],  working_state[14])

    # Add the initial state to the mixed state to create the final keystream block
    final_state = [(working_state[i] + state[i]) & 0xffffffff for i in range(16)]

    # Serialize the state into a 64-byte little-endian byte string
    return struct.pack("<16I", *final_state)

def chacha20_crypt(key: bytes, nonce: bytes, data: bytes, start_counter: int = 1) -> bytes:
    """
    Encrypts or decrypts data using the ChaCha20 stream cipher.
    The operation is symmetrical (XOR), so the same function is used for both.
    """
    output = bytearray()
    counter = start_counter
    for i in range(0, len(data), 64):
        keystream_block = chacha20_block_generator(key, counter, nonce)
        chunk = data[i:i+64]
        # XOR the data chunk with the keystream block
        output.extend(byte ^ keystream_byte for byte, keystream_byte in zip(chunk, keystream_block))
        counter += 1
    return bytes(output)

# ==============================================================================
# === ChaCha20 Visualizer Class
# ==============================================================================

class ChaCha20Visualizer:
    """A class to provide a step-by-step visualization of the ChaCha20 block function."""
    def __init__(self, key: bytes, counter: int, nonce: bytes, plaintext: bytes):
        self.key = key
        self.counter = counter
        self.nonce = nonce
        self.plaintext_block = plaintext[:64].ljust(64, b'\0')

        self.constants = (0x61707865, 0x3320646e, 0x79622d32, 0x6b206574)
        self.initial_state = list(self.constants +
                                  struct.unpack("<8I", self.key) +
                                  (self.counter,) +
                                  struct.unpack("<3I", self.nonce))
        self.state = self.initial_state[:]

    @staticmethod
    def _clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def _pause(self, seconds=1.5):
        time.sleep(seconds)

    def _print_state(self, title: str, highlights: List[int] = None, old_state: List[int] = None):
        """Prints the 4x4 state matrix with optional highlighting for changed values."""
        print(f"\n--- {Colors.BOLD}{title}{Colors.RESET} ---")
        matrix_map = [
            (f"{Colors.CYAN}const", [0, 1, 2, 3]),
            (f"{Colors.YELLOW}key", [4, 5, 6, 7, 8, 9, 10, 11]),
            (f"{Colors.MAGENTA}counter", [12]),
            (f"{Colors.BLUE}nonce", [13, 14, 15])
        ]
        
        for i in range(4):
            row_str = []
            for j in range(4):
                idx = i * 4 + j
                val = self.state[idx]
                val_str = f"0x{val:08x}"
                
                color = ""
                for name, indices in matrix_map:
                    if idx in indices:
                        color = name
                        break
                
                # If an old state is provided, highlight changes in green
                if old_state and val != old_state[idx]:
                    val_str = f"{Colors.GREEN}{val_str}"
                # If specific indices are to be highlighted (e.g., a quarter round)
                elif highlights and idx in highlights:
                     val_str = f"{Colors.GREEN}{val_str}"
                else:
                    val_str = f"{color}{val_str}"

                row_str.append(val_str + Colors.RESET)
            print(" | ".join(row_str))
        print("-" * 55)

    def _run_quarter_round_visual(self, indices: Tuple[int, int, int, int], description: str):
        """Visualizes a single quarter_round operation."""
        a, b, c, d = indices
        print(f"\n{Colors.BOLD}Applying Quarter Round to {description}: indices ({a}, {b}, {c}, {d}){Colors.RESET}")
        
        old_state = self.state[:]
        self._print_state("State BEFORE Quarter Round", highlights=list(indices))
        self._pause()
        
        self.state[a], self.state[b], self.state[c], self.state[d] = quarter_round(
            self.state[a], self.state[b], self.state[c], self.state[d]
        )
        self._print_state("State AFTER Quarter Round", old_state=old_state)
        self._pause(2)

    def run(self):
        """Starts the full visualization process."""
        self._clear()
        print(f"{Colors.BOLD}=== ChaCha20 Block Function Visualization ==={Colors.RESET}")
        self._print_state("Step 1: Initial State Construction")
        print(f"{Colors.CYAN}■ Constants{Colors.RESET} | {Colors.YELLOW}■ Key{Colors.RESET} | {Colors.MAGENTA}■ Counter{Colors.RESET} | {Colors.BLUE}■ Nonce{Colors.RESET}")
        input("\nPress Enter to begin the rounds...")

        for i in range(10):
            self._clear()
            print(f"{Colors.BOLD}=== ROUND {i + 1} of 10 ==={Colors.RESET}")
            
            # Column Round
            self._run_quarter_round_visual((0, 4, 8, 12), "Column 1")
            self._run_quarter_round_visual((1, 5, 9, 13), "Column 2")
            self._run_quarter_round_visual((2, 6, 10, 14), "Column 3")
            self._run_quarter_round_visual((3, 7, 11, 15), "Column 4")
            
            # Diagonal Round
            self._run_quarter_round_visual((0, 5, 10, 15), "Diagonal 1")
            self._run_quarter_round_visual((1, 6, 11, 12), "Diagonal 2")
            self._run_quarter_round_visual((2, 7, 8, 13), "Diagonal 3")
            self._run_quarter_round_visual((3, 4, 9, 14), "Diagonal 4")

            if i < 9:
                input(f"End of Round {i + 1}. Press Enter to continue to the next round...")

        # Final addition
        self._clear()
        print(f"{Colors.BOLD}=== Final Steps ==={Colors.RESET}")
        print("\nStep 2: Add Initial State to the final mixed state.")
        print("This prevents reversing the rounds to find the pre-addition state.")
        self._print_state("Final Mixed State (before addition)")
        self._pause()
        final_block_state = [(self.state[i] + self.initial_state[i]) & 0xffffffff for i in range(16)]
        self.state = final_block_state # Update state to the final keystream
        self._print_state("Final Keystream Block (after addition)", old_state=self.initial_state)
        input("Press Enter to proceed to the final XOR encryption...")

        # XOR operation
        self._clear()
        print(f"{Colors.BOLD}Step 3: XOR Plaintext with Keystream{Colors.RESET}")
        keystream_bytes = struct.pack("<16I", *self.state)
        ciphertext_bytes = bytes(p ^ k for p, k in zip(self.plaintext_block, keystream_bytes))

        print("\nPLAINTEXT  (P) | KEYSTREAM  (K) | CIPHERTEXT (C = P ⊕ K)")
        print("-----------------+------------------+-------------------------")
        for i in range(0, 64, 16):
            p_chunk = self.plaintext_block[i:i+16]
            k_chunk = keystream_bytes[i:i+16]
            c_chunk = ciphertext_bytes[i:i+16]
            print(f"{Colors.YELLOW}{p_chunk.hex(' ')}{Colors.RESET} | "
                  f"{Colors.CYAN}{k_chunk.hex(' ')}{Colors.RESET} | "
                  f"{Colors.GREEN}{c_chunk.hex(' ')}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Final Ciphertext (hex):{Colors.RESET} {ciphertext_bytes.hex()}")

# ==============================================================================
# === Main Application Logic
# ==============================================================================

def quick_demo():
    """A simple, non-visual demonstration of ChaCha20."""
    print(f"\n{Colors.BOLD}--- ChaCha20 Quick Demonstration ---{Colors.RESET}")
    try:
        key_input = input("Enter a key (up to 32 chars, will be padded/truncated): ").encode()
        plaintext = input("Enter your plaintext message: ").encode()

        key = key_input.ljust(32, b'\0')[:32]
        nonce = os.urandom(12)  # A secure, random 12-byte nonce

        print("\n[CONFIG]")
        print(f"  Key (32 bytes):      {Colors.YELLOW}{key.hex()}{Colors.RESET}")
        print(f"  Nonce (12 bytes):    {Colors.BLUE}{nonce.hex()}{Colors.RESET} (Randomly generated)")
        print(f"  Plaintext:           '{plaintext.decode(errors='ignore')}'")

        print("\n[ENCRYPTION]")
        ciphertext = chacha20_crypt(key, nonce, plaintext)
        print(f"  Ciphertext (hex):    {Colors.GREEN}{ciphertext.hex()}{Colors.RESET}")

        print("\n[DECRYPTION]")
        decrypted = chacha20_crypt(key, nonce, ciphertext)
        print(f"  Decrypted text:      '{decrypted.decode(errors='ignore')}'")

        assert plaintext == decrypted
        print(f"\n{Colors.BOLD}{Colors.GREEN}Success!{Colors.RESET} Decrypted text matches original plaintext.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    """Main function to run the educational tool."""
    while True:
        ChaCha20Visualizer._clear()
        print(f"{Colors.BOLD}Welcome to the ChaCha20 Educational Tool{Colors.RESET}")
        print("This program can demonstrate the ChaCha20 stream cipher.")
        print("\nChoose an option:")
        print("  (1) Quick Demonstration (Encrypt & Decrypt)")
        print("  (2) Detailed Visualization (with your own data)")
        print("  (3) RFC 7539 Test Vector Visualization (Standard Example)")
        print("  (4) Exit")
        choice = input("\nEnter your choice [1-4]: ").strip()

        if choice == '1':
            quick_demo()
            input("\nPress Enter to return to the menu.")

        elif choice == '2':
            print(f"\n{Colors.BOLD}--- Custom Data for Visualization ---{Colors.RESET}")
            key_input = input("Enter a key (up to 32 chars): ").encode()
            key = key_input.ljust(32, b'\0')[:32]
            plaintext = input("Enter a short plaintext (up to 64 chars): ").encode()
            nonce = os.urandom(12)
            counter = 1
            
            visualizer = ChaCha20Visualizer(key, counter, nonce, plaintext)
            visualizer.run()
            print(f"\n{Colors.BOLD}Visualization Complete.{Colors.RESET}")
            if len(plaintext) > 64:
                print("Note: The visualization only showed the process for the first 64-byte block.")
                print("For subsequent blocks, the counter would increment and the process would repeat.")
            input("\nPress Enter to return to the menu.")

        elif choice == '3':
            print(f"\n{Colors.BOLD}--- RFC 7539 Test Vector Visualization ---{Colors.RESET}")
            print("Using the standard test vector from the official ChaCha20 specification.")
            # Key: 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
            key = bytes(range(32))
            # Nonce: 000000090000004a00000000 (Note: RFC uses 8-byte nonce and 8-byte counter,
            # but modern usage is 12-byte nonce and 4-byte counter. We adapt it.)
            # Nonce: 000000000000004a00000000
            nonce = b'\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00'
            counter = 1
            plaintext = (
                b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip "
                b"for the future, sunscreen would be it."
            )
            
            visualizer = ChaCha20Visualizer(key, counter, nonce, plaintext)
            visualizer.run()
            print(f"\n{Colors.BOLD}Visualization Complete.{Colors.RESET}")
            input("\nPress Enter to return to the menu.")

        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()