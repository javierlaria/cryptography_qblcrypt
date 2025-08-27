#!/usr/bin/env python3
"""
ChaCha20 Educational Demonstration
Professor's Edition - Designed for Classroom Teaching
"""

import os
import struct
import time
from typing import List, Tuple, Optional

# ANSI color codes for terminal output
COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

class ChaCha20Core:
    """Core ChaCha20 implementation with no side effects (for actual encryption)"""
    CONSTANTS = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]  # "expand 32-byte k"
    
    @staticmethod
    def rotl32(x: int, n: int) -> int:
        """32-bit rotate left"""
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

    @staticmethod
    def quarter_round(a: int, b: int, c: int, d: int) -> Tuple[int, int, int, int]:
        """Perform one ChaCha20 quarter round (all 4 steps)"""
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = ChaCha20Core.rotl32(d, 16)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = ChaCha20Core.rotl32(b, 12)
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = ChaCha20Core.rotl32(d, 8)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = ChaCha20Core.rotl32(b, 7)
        return a, b, c, d

    @staticmethod
    def chacha20_block(key: List[int], counter: int, nonce: List[int]) -> List[int]:
        """Generate one 64-byte ChaCha20 block (core algorithm)"""
        # Initialize state
        state = ChaCha20Core.CONSTANTS + key + [counter] + nonce
        working_state = state.copy()

        # Perform 20 rounds (10 double rounds)
        for _ in range(10):
            # Column rounds
            working_state[0], working_state[4], working_state[8], working_state[12] = ChaCha20Core.quarter_round(
                working_state[0], working_state[4], working_state[8], working_state[12])
            working_state[1], working_state[5], working_state[9], working_state[13] = ChaCha20Core.quarter_round(
                working_state[1], working_state[5], working_state[9], working_state[13])
            working_state[2], working_state[6], working_state[10], working_state[14] = ChaCha20Core.quarter_round(
                working_state[2], working_state[6], working_state[10], working_state[14])
            working_state[3], working_state[7], working_state[11], working_state[15] = ChaCha20Core.quarter_round(
                working_state[3], working_state[7], working_state[11], working_state[15])
            
            # Diagonal rounds
            working_state[0], working_state[5], working_state[10], working_state[15] = ChaCha20Core.quarter_round(
                working_state[0], working_state[5], working_state[10], working_state[15])
            working_state[1], working_state[6], working_state[11], working_state[12] = ChaCha20Core.quarter_round(
                working_state[1], working_state[6], working_state[11], working_state[12])
            working_state[2], working_state[7], working_state[8], working_state[13] = ChaCha20Core.quarter_round(
                working_state[2], working_state[7], working_state[8], working_state[13])
            working_state[3], working_state[4], working_state[9], working_state[14] = ChaCha20Core.quarter_round(
                working_state[3], working_state[4], working_state[9], working_state[14])

        # Add initial state
        for i in range(16):
            working_state[i] = (working_state[i] + state[i]) & 0xFFFFFFFF

        return working_state

    @staticmethod
    def chacha20_encrypt(key: bytes, nonce: bytes, plaintext: bytes, counter_start: int = 1) -> bytes:
        """Encrypt plaintext using ChaCha20"""
        key_words = struct.unpack('<8I', key)
        nonce_words = struct.unpack('<3I', nonce)
        ciphertext = bytearray()
        counter = counter_start
        
        for block_start in range(0, len(plaintext), 64):
            block = ChaCha20Core.chacha20_block(key_words, counter, nonce_words)
            counter += 1
            block_bytes = struct.pack('<16I', *block)
            block_len = min(64, len(plaintext) - block_start)
            
            for i in range(block_len):
                ciphertext.append(plaintext[block_start + i] ^ block_bytes[i])
                
        return bytes(ciphertext)


class ChaCha20Animator:
    """Step-by-step animation of ChaCha20 block generation with educational explanations"""
    
    def __init__(self):
        self.state = [0] * 16
        self.initial_state = [0] * 16
        self.key = [0] * 8
        self.nonce = [0] * 3
        self.counter = 0
        self.quarter_round_sequence = self._generate_quarter_round_sequence()
        self.current_step = 0
        self.current_operation = 0
        self.current_round = 0
        self.total_steps = 80 * 4  # 10 rounds * 8 quarter rounds * 4 operations

    def _generate_quarter_round_sequence(self) -> List[Tuple[int, int, int, int]]:
        """Generate sequence of quarter rounds (80 total)"""
        column_rounds = [
            (0, 4, 8, 12), (1, 5, 9, 13), 
            (2, 6, 10, 14), (3, 7, 11, 15)
        ]
        diagonal_rounds = [
            (0, 5, 10, 15), (1, 6, 11, 12),
            (2, 7, 8, 13), (3, 4, 9, 14)
        ]
        sequence = []
        for _ in range(10):
            sequence.extend(column_rounds)
            sequence.extend(diagonal_rounds)
        return sequence

    def initialize(self, key: bytes, counter: int, nonce: bytes):
        """Initialize state with key, counter, and nonce"""
        # Convert inputs to word arrays
        self.key = list(struct.unpack('<8I', key))
        self.nonce = list(struct.unpack('<3I', nonce))
        self.counter = counter
        
        # Build initial state
        self.state = ChaCha20Core.CONSTANTS + self.key + [counter] + self.nonce
        self.initial_state = self.state.copy()
        self.current_step = 0
        self.current_operation = 0
        self.current_round = 0

    def get_step_info(self) -> Tuple[str, str, List[int], str]:
        """Get current step information for display"""
        if self.current_step >= self.total_steps:
            return "Finalization", "Adding initial state to working state", list(range(16)), ""
        
        # Calculate current position in algorithm
        round_num = self.current_step // 32  # 32 operations per double round
        quarter_round = (self.current_step % 32) // 4
        operation = self.current_step % 4
        
        # Determine round type
        round_type = "Column" if quarter_round < 4 else "Diagonal"
        quarter_in_type = quarter_round % 4
        
        # Get current quarter round indices
        q_round_idx = self.current_step // 4
        indices = list(self.quarter_round_sequence[q_round_idx])
        
        # Operation description
        op_desc = [
            "a = (a + b) mod 2³²; d = d XOR a; d = ROTL(d, 16)",
            "c = (c + d) mod 2³²; b = b XOR c; b = ROTL(b, 12)",
            "a = (a + b) mod 2³²; d = d XOR a; d = ROTL(d, 8)",
            "c = (c + d) mod 2³²; b = b XOR c; b = ROTL(b, 7)"
        ][operation]
        
        title = f"Double Round {round_num+1}/10 | {round_type} Round {quarter_in_type+1}/4 | Step {operation+1}/4"
        explanation = (
            f"Quarter Round: {indices}\n"
            f"Values: x{indices[0]}=0x{self.state[indices[0]]:08x}, "
            f"x{indices[1]}=0x{self.state[indices[1]]:08x}, "
            f"x{indices[2]}=0x{self.state[indices[2]]:08x}, "
            f"x{indices[3]}=0x{self.state[indices[3]]:08x}"
        )
        
        return title, op_desc, indices, explanation

    def step(self) -> bool:
        """Perform one operation in the ChaCha20 algorithm"""
        if self.current_step >= self.total_steps:
            return False
            
        # Get current quarter round
        q_round_idx = self.current_step // 4
        a, b, c, d = self.quarter_round_sequence[q_round_idx]
        op = self.current_step % 4
        
        # Execute one operation of the quarter round
        if op == 0:
            self.state[a] = (self.state[a] + self.state[b]) & 0xFFFFFFFF
            self.state[d] ^= self.state[a]
            self.state[d] = ChaCha20Core.rotl32(self.state[d], 16)
        elif op == 1:
            self.state[c] = (self.state[c] + self.state[d]) & 0xFFFFFFFF
            self.state[b] ^= self.state[c]
            self.state[b] = ChaCha20Core.rotl32(self.state[b], 12)
        elif op == 2:
            self.state[a] = (self.state[a] + self.state[b]) & 0xFFFFFFFF
            self.state[d] ^= self.state[a]
            self.state[d] = ChaCha20Core.rotl32(self.state[d], 8)
        elif op == 3:
            self.state[c] = (self.state[c] + self.state[d]) & 0xFFFFFFFF
            self.state[b] ^= self.state[c]
            self.state[b] = ChaCha20Core.rotl32(self.state[b], 7)
        
        self.current_step += 1
        return True

    def finalize(self):
        """Perform final state addition"""
        for i in range(16):
            self.state[i] = (self.state[i] + self.initial_state[i]) & 0xFFFFFFFF

    def display_state(self, title: str, highlight: Optional[List[int]] = None, 
                     explanation: str = "", delay: float = 0.0):
        """Display the current state matrix with highlighting"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{COLORS['HEADER']}{title}{COLORS['ENDC']}")
        print("+" + "-" * 53 + "+")
        
        for i in range(0, 16, 4):
            row = []
            for j in range(4):
                idx = i + j
                value = f"0x{self.state[idx]:08x}"
                if highlight and idx in highlight:
                    value = f"{COLORS['OKGREEN']}{value}{COLORS['ENDC']}"
                row.append(value)
            print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
        
        print("+" + "-" * 53 + "+")
        
        # Matrix positions
        print("| (0,0) | (0,1) | (0,2) | (0,3) |  Column Round Indices:")
        print("| (1,0) | (1,1) | (1,2) | (1,3) |    (0,4,8,12), (1,5,9,13)")
        print("| (2,0) | (2,1) | (2,2) | (2,3) |    (2,6,10,14), (3,7,11,15)")
        print("| (3,0) | (3,1) | (3,2) | (3,3) |  Diagonal Round Indices:")
        print("+" + "-" * 53 + "+")  #    (0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14)")
        
        if explanation:
            print(f"\n{COLORS['OKBLUE']}{explanation}{COLORS['ENDC']}")
        
        if delay > 0:
            time.sleep(delay)

    def display_binary(self, value: int, title: str):
        """Display binary representation of a 32-bit value"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{COLORS['HEADER']}{title}{COLORS['ENDC']}")
        print("+" + "-" * 73 + "+")
        binary = format(value, '032b')
        hex_val = f"0x{value:08x}"
        
        print(f"| Decimal: {value:<10} | Hex: {hex_val} | Binary: {binary} |")
        print("+" + "-" * 73 + "+")
        
        # Show bit positions
        bit_positions = "31        24        16         8         0"
        print(f"| {bit_positions} |")
        print("+" + "-" * 73 + "+")
        
        # Show byte breakdown
        bytes_repr = [
            f"Byte 3: {binary[0:8]} (0x{value >> 24:02x})",
            f"Byte 2: {binary[8:16]} (0x{(value >> 16) & 0xFF:02x})",
            f"Byte 1: {binary[16:24]} (0x{(value >> 8) & 0xFF:02x})",
            f"Byte 0: {binary[24:32]} (0x{value & 0xFF:02x})"
        ]
        
        for b in bytes_repr:
            print(f"| {b:<69} |")
        print("+" + "-" * 73 + "+")
        
        input("\nPress Enter to continue...")

    def run_animation(self, auto_advance: bool = False):
        """Run the full animation sequence"""
        # Initial state
        self.display_state(
            "CHA-CHA-20 BLOCK GENERATION - INITIAL STATE",
            explanation=(
                "State Matrix Structure:\n"
                "  [ Constants ]  [ Key (8 words) ]\n"
                "  [ Counter   ]  [ Nonce (3 words) ]\n\n"
                "Constants: 'expa' (0x61707865), 'nd 3' (0x3320646e),\n"
                "           '2-by' (0x79622d32), 'te k' (0x6b206574)\n"
                "Key: 32-byte secret key (8 words)\n"
                "Counter: Block counter (starts at 1)\n"
                "Nonce: 96-bit public number (3 words)"
            )
        )
        input("\nPress Enter to start animation (Ctrl+C to skip)...") if not auto_advance else time.sleep(2)
        
        # Step through all operations
        try:
            for step in range(self.total_steps):
                title, op_desc, highlight, explanation = self.get_step_info()
                self.display_state(title, highlight, explanation + f"\n\n{op_desc}")
                
                if auto_advance:
                    time.sleep(0.3)
                else:
                    input("\nPress Enter for next step (Ctrl+C to skip)...")

                self.step()
        except KeyboardInterrupt:
            print("\nAnimation skipped. Generating final state...")
            while self.step():
                pass

        # Final state addition
        self.finalize()
        self.display_state(
            "FINAL STATE (AFTER ADDING INITIAL STATE)",
            explanation=(
                "Final Step: Working State + Initial State (mod 2³²)\n\n"
                "This prevents reversing the cipher and ensures:\n"
                "1. Non-linearity\n"
                "2. Diffusion of initial state\n"
                "3. Resistance to cryptanalysis"
            )
        )
        input("\nPress Enter to see keystream bytes...")


class ProfessorDemo:
    """Main demonstration controller for classroom teaching"""
    
    def __init__(self):
        self.key = b""
        self.nonce = b""
        self.plaintext = b""
        self.ciphertext = b""
        self.decrypted = b""
        self.animator = ChaCha20Animator()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title: str):
        self.clear_screen()
        print(f"\n{COLORS['HEADER']}{COLORS['BOLD']}{'=' * 50}")
        print(f"{title.upper()}")
        print(f"{'=' * 50}{COLORS['ENDC']}\n")
    
    def get_key_input(self):
        self.display_header("KEY SELECTION")
        print("ChaCha20 uses a 256-bit (32-byte) key")
        print("1. Use RFC 7539 test vector (recommended for learning)")
        print("2. Enter custom ASCII key (padded to 32 characters)")
        print("3. Enter custom hex key (64 hex digits)")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            # RFC 7539 test vector
            self.key = bytes.fromhex(
                "03020100070605040b0a09080f0e0d0c"
                "13121110171615141b1a19181f1e1d1c"
            )
            print(f"\n{COLORS['OKGREEN']}Using RFC 7539 test vector key{COLORS['ENDC']}")
            print(f"Key (hex): {self.key.hex()}")
            
        elif choice == '2':
            key_str = input("\nEnter 32-character key: ").ljust(32)[:32]
            self.key = key_str.encode('utf-8')
            print(f"\nKey (hex): {self.key.hex()}")
            print(f"Key as ASCII: '{key_str}'")
            
        else:
            hex_key = input("\nEnter 64 hex digits: ").strip().lower()
            if len(hex_key) != 64 or not all(c in "0123456789abcdef" for c in hex_key):
                print(f"{COLORS['FAIL']}Invalid hex key! Using default test vector{COLORS['ENDC']}")
                self.get_key_input()
                return
            self.key = bytes.fromhex(hex_key)
            print(f"\nKey (hex): {self.key.hex()}")
        
        input("\nPress Enter to continue...")
    
    def get_nonce_input(self):
        self.display_header("NONCE SELECTION")
        print("ChaCha20 uses a 96-bit (12-byte) nonce")
        print("1. Use RFC 7539 test vector nonce")
        print("2. Generate random nonce")
        print("3. Enter custom hex nonce (24 hex digits)")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            # RFC 7539 test vector
            self.nonce = bytes.fromhex("00000000000000004a000000")
            print(f"\n{COLORS['OKGREEN']}Using RFC 7539 test vector nonce{COLORS['ENDC']}")
            
        elif choice == '2':
            self.nonce = os.urandom(12)
            print(f"\nGenerated random nonce (hex): {self.nonce.hex()}")
            
        else:
            hex_nonce = input("\nEnter 24 hex digits: ").strip().lower()
            if len(hex_nonce) != 24 or not all(c in "0123456789abcdef" for c in hex_nonce):
                print(f"{COLORS['FAIL']}Invalid hex nonce! Using random nonce{COLORS['ENDC']}")
                self.nonce = os.urandom(12)
                print(f"Generated random nonce (hex): {self.nonce.hex()}")
            else:
                self.nonce = bytes.fromhex(hex_nonce)
        
        input("\nPress Enter to continue...")
    
    def get_plaintext_input(self):
        self.display_header("PLAINTEXT SELECTION")
        print("Enter your plaintext message (will be padded to block size)")
        print("1. Use 'Hello, ChaCha20! This is a test message.'")
        print("2. Enter custom text")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            self.plaintext = b"Hello, ChaCha20! This is a test message."
        else:
            self.plaintext = input("\nEnter plaintext: ").encode('utf-8')
        
        print(f"\nPlaintext (hex): {self.plaintext.hex()}")
        print(f"Plaintext as ASCII: {self.plaintext.decode('ascii', 'replace')}")
        input("\nPress Enter to continue...")
    
    def demonstrate_core_concepts(self):
        self.display_header("CORE CRYPTOGRAPHIC CONCEPTS")
        print("CHA-CHA-20 DESIGN PRINCIPLES:\n")
        
        concepts = [
            ("ARX Operations", 
             "Uses only Addition, Rotation, XOR - no S-boxes\n"
             "✓ Efficient in software\n"
             "✓ Resistant to cache timing attacks\n"
             "✓ Simple hardware implementation"),
            
            ("20-Round Structure",
             "10 double rounds (column + diagonal)\n"
             "✓ Provides strong diffusion\n"
             "✓ Each bit affects all output bits in 3 rounds\n"
             "✓ Security margin against cryptanalysis"),
            
            ("Quarter Round",
             "Core transformation:\n"
             "  a += b; d ^= a; d = ROTL(d,16)\n"
             "  c += d; b ^= c; b = ROTL(b,12)\n"
             "  a += b; d ^= a; d = ROTL(d,8)\n"
             "  c += d; b ^= c; b = ROTL(b,7)\n"
             "✓ Non-linear mixing\n"
             "✓ Fast diffusion"),
            
            ("Final State Addition",
             "Working State + Initial State (mod 2³²)\n"
             "✓ Prevents reversing the cipher\n"
             "✓ Ensures initial state affects output\n"
             "✓ Critical for security")
        ]
        
        for i, (title, desc) in enumerate(concepts, 1):
            print(f"{COLORS['OKBLUE']}{i}. {title}{COLORS['ENDC']}")
            for line in desc.split('\n'):
                print(f"   {line}")
            print()
        
        input("\nPress Enter to see the Quarter Round in detail...")
        
        # Show quarter round operations
        sample_state = [
            0x11111111, 0x01020304, 0x95969798, 0x01234567,
            0x22222222, 0x05060708, 0x999A9B9C, 0x89ABCDEF,
            0x33333333, 0x090A0B0C, 0x9D9E9F00, 0xFEDCBA98,
            0x44444444, 0x0D0E0F10, 0x01020304, 0x76543210
        ]
        
        a, b, c, d = 0, 4, 8, 12
        working = sample_state.copy()
        
        steps = [
            ("Initial State", ""),
            ("a = a + b", 
             f"0x{working[a]:08x} + 0x{working[b]:08x} = 0x{((working[a] + working[b]) & 0xFFFFFFFF):08x}"),
            ("d = d XOR a", 
             f"0x{working[d]:08x} XOR 0x{working[a]:08x} = 0x{(working[d] ^ working[a]):08x}"),
            ("d = ROTL(d, 16)", 
             f"ROTL(0x{working[d]:08x}, 16) = 0x{ChaCha20Core.rotl32(working[d], 16):08x}"),
            ("c = c + d", 
             f"0x{working[c]:08x} + 0x{working[d]:08x} = 0x{((working[c] + working[d]) & 0xFFFFFFFF):08x}"),
            ("b = b XOR c", 
             f"0x{working[b]:08x} XOR 0x{working[c]:08x} = 0x{(working[b] ^ working[c]):08x}"),
            ("b = ROTL(b, 12)", 
             f"ROTL(0x{working[b]:08x}, 12) = 0x{ChaCha20Core.rotl32(working[b], 12):08x}"),
            ("a = a + b", 
             f"0x{working[a]:08x} + 0x{working[b]:08x} = 0x{((working[a] + working[b]) & 0xFFFFFFFF):08x}"),
            ("d = d XOR a", 
             f"0x{working[d]:08x} XOR 0x{working[a]:08x} = 0x{(working[d] ^ working[a]):08x}"),
            ("d = ROTL(d, 8)", 
             f"ROTL(0x{working[d]:08x}, 8) = 0x{ChaCha20Core.rotl32(working[d], 8):08x}"),
            ("c = c + d", 
             f"0x{working[c]:08x} + 0x{working[d]:08x} = 0x{((working[c] + working[d]) & 0xFFFFFFFF):08x}"),
            ("b = b XOR c", 
             f"0x{working[b]:08x} XOR 0x{working[c]:08x} = 0x{(working[b] ^ working[c]):08x}"),
            ("b = ROTL(b, 7)", 
             f"ROTL(0x{working[b]:08x}, 7) = 0x{ChaCha20Core.rotl32(working[b], 7):08x}")
        ]
        
        for i, (title, calc) in enumerate(steps):
            # Update state for current step
            if i == 1:
                working[a] = (working[a] + working[b]) & 0xFFFFFFFF
            elif i == 2:
                working[d] ^= working[a]
            elif i == 3:
                working[d] = ChaCha20Core.rotl32(working[d], 16)
            elif i == 4:
                working[c] = (working[c] + working[d]) & 0xFFFFFFFF
            elif i == 5:
                working[b] ^= working[c]
            elif i == 6:
                working[b] = ChaCha20Core.rotl32(working[b], 12)
            elif i == 7:
                working[a] = (working[a] + working[b]) & 0xFFFFFFFF
            elif i == 8:
                working[d] ^= working[a]
            elif i == 9:
                working[d] = ChaCha20Core.rotl32(working[d], 8)
            elif i == 10:
                working[c] = (working[c] + working[d]) & 0xFFFFFFFF
            elif i == 11:
                working[b] ^= working[c]
            elif i == 12:
                working[b] = ChaCha20Core.rotl32(working[b], 7)
            
            # Display
            self.clear_screen()
            print(f"\n{COLORS['HEADER']}QUARTER ROUND STEP-BY-STEP: {title}{COLORS['ENDC']}")
            print(f"Indices: a={a}, b={b}, c={c}, d={d}")
            if calc:
                print(f"Calculation: {calc}\n")
            
            # Display state with highlights
            print("+" + "-" * 53 + "+")
            for row in range(4):
                cells = []
                for col in range(4):
                    idx = col * 4 + row
                    val = f"0x{working[idx]:08x}"
                    if idx in [a, b, c, d]:
                        val = f"{COLORS['OKGREEN']}{val}{COLORS['ENDC']}"
                    cells.append(val)
                print(f"| {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |")
            print("+" + "-" * 53 + "+")
            
            input(f"\nPress Enter for {'next' if i < len(steps)-1 else 'final'} step...")
    
    def run_animation_demo(self):
        self.display_header("BLOCK GENERATION ANIMATION")
        print("This animation shows how ChaCha20 generates a keystream block")
        print("Key concepts demonstrated:")
        print("  - State matrix initialization")
        print("  - Column and diagonal rounds")
        print("  - Quarter round operations")
        print("  - Final state addition\n")
        
        auto = input("Run in auto-advance mode? (y/n): ").strip().lower() == 'y'
        
        self.animator.initialize(self.key, 1, self.nonce)
        self.animator.run_animation(auto_advance=auto)
        
        # Show keystream bytes
        keystream = struct.pack('<16I', *self.animator.state)
        self.display_header("GENERATED KEYSTREAM (FIRST 32 BYTES)")
        print("Keystream is used to XOR with plaintext:\n")
        
        for i in range(0, 32, 16):
            hex_line = ' '.join(f'{b:02x}' for b in keystream[i:i+16])
            print(f"Bytes {i:2d}-{i+15:2d}: {hex_line}")
        
        print("\nThis keystream is combined with plaintext using XOR:")
        print("  Ciphertext = Plaintext ⊕ Keystream")
        input("\nPress Enter to continue...")
    
    def run_encryption_demo(self):
        self.display_header("FULL ENCRYPTION DEMONSTRATION")
        
        # Encrypt
        self.ciphertext = ChaCha20Core.chacha20_encrypt(self.key, self.nonce, self.plaintext)
        
        # Decrypt
        self.decrypted = ChaCha20Core.chacha20_encrypt(self.key, self.nonce, self.ciphertext)
        
        # Display results
        print("KEY (32 bytes):")
        print(self.key.hex())
        
        print("\nNONCE (12 bytes):")
        print(self.nonce.hex())
        
        print("\nPLAINTEXT:")
        print(f"  Hex: {self.plaintext.hex()}")
        print(f"  ASCII: {self.plaintext.decode('ascii', 'replace')}")
        
        print("\nCIPHERTEXT:")
        print(f"  Hex: {self.ciphertext.hex()}")
        
        print("\nDECRYPTED TEXT:")
        print(f"  Hex: {self.decrypted.hex()}")
        print(f"  ASCII: {self.decrypted.decode('ascii', 'replace')}")
        
        # Verify
        status = COLORS['OKGREEN'] + "SUCCESS" + COLORS['ENDC'] if self.plaintext == self.decrypted else COLORS['FAIL'] + "FAILED" + COLORS['ENDC']
        print(f"\n{COLORS['BOLD']}Decryption verification: {status}{COLORS['ENDC']}")
        
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        while True:
            self.display_header("CHA-CHA-20 EDUCATIONAL DEMONSTRATION")
            print("1. Learn core cryptographic concepts")
            print("2. Run block generation animation")
            print("3. Perform full encryption/decryption demo")
            print("4. Exit\n")
            
            choice = input("Select an option: ").strip()
            
            if choice == '1':
                self.demonstrate_core_concepts()
            elif choice == '2':
                if not self.key: self.get_key_input()
                if not self.nonce: self.get_nonce_input()
                self.run_animation_demo()
            elif choice == '3':
                if not self.key: self.get_key_input()
                if not self.nonce: self.get_nonce_input()
                if not self.plaintext: self.get_plaintext_input()
                self.run_encryption_demo()
            elif choice == '4':
                print("\nThank you for using the ChaCha20 Educational Demonstration!")
                break
            else:
                input("Invalid choice. Press Enter to try again...")


if __name__ == "__main__":
    print(f"{COLORS['HEADER']}{'='*60}")
    print("CHA-CHA-20 CRYPTOGRAPHIC DEMONSTRATION - PROFESSOR'S EDITION")
    print("Designed for Classroom Teaching | RFC 7539 Compliant")
    print(f"{'='*60}{COLORS['ENDC']}")
    print("\nThis demonstration shows:")
    print("✓ Step-by-step block generation")
    print("✓ Core cryptographic principles")
    print("✓ Full encryption/decryption process")
    print("✓ Real-world test vectors (RFC 7539)")
    print("\nPress Ctrl+C at any time to skip animations")
    
    input(f"\n{COLORS['WARNING']}Press Enter to begin the demonstration...{COLORS['ENDC']}")
    
    demo = ProfessorDemo()
    demo.main_menu()