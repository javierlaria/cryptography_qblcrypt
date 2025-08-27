#!/usr/bin/env python3
"""
AES-128 Interactive Step-by-Step Demonstration with Enhanced Explanations
"""

import os
import time
import sys

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

# S-box
sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Inverse S-box
inv_sbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Round constants
rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

# Utility functions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_bytes_hex(label, data):
    print(f"{label}: {' '.join(f'{b:02x}' for b in data)}")

def pad(data):
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)

def unpad(data):
    padding_len = data[-1]
    if padding_len == 0 or padding_len > 16:
        raise ValueError("Invalid padding")
    if all(b == padding_len for b in data[-padding_len:]):
        return data[:-padding_len]
    raise ValueError("Invalid padding")

def gf_mult(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xff
        if hi_bit:
            a ^= 0x1b
        b >>= 1
    return p

def bytes_to_state(bytes_in):
    state = [[0] * 4 for _ in range(4)]
    for c in range(4):
        for r in range(4):
            state[r][c] = bytes_in[r + 4 * c]
    return state

def state_to_bytes(state):
    bytes_out = bytearray(16)
    for c in range(4):
        for r in range(4):
            bytes_out[r + 4 * c] = state[r][c]
    return bytes_out

def print_state_diff(label, state, prev_state=None):
    print(label)
    print("  Col0 Col1 Col2 Col3")  # Added column labels
    for r in range(4):
        row_str = [f"Row{r}:"]
        for c in range(4):
            val_str = f'{state[r][c]:02x}'
            if prev_state and state[r][c] != prev_state[r][c]:
                val_str = f'{RED}{val_str}{RESET}'
            row_str.append(val_str)
        print(' '.join(row_str))

def print_word(label, word):
    print(f"{label}: {word >> 24:02x} { (word >> 16) & 0xff :02x} { (word >> 8) & 0xff :02x} {word & 0xff :02x}")

# AES operations with enhanced explanations

def sub_bytes(state):
    print("\nSubBytes Explanation: This step introduces non-linearity and confusion. Each byte in the 4x4 state matrix is replaced by its corresponding value in the S-box, which is a lookup table derived from the multiplicative inverse in GF(2^8) followed by an affine transformation.")
    print("Example: For a byte like 0x53, S-box[0x53] = 0xed")
    for r in range(4):
        for c in range(4):
            state[r][c] = sbox[state[r][c]]

def inv_sub_bytes(state):
    print("\nInvSubBytes Explanation: The inverse of SubBytes, using the inverse S-box to revert the substitution.")
    for r in range(4):
        for c in range(4):
            state[r][c] = inv_sbox[state[r][c]]

def shift_rows(state):
    print("\nShiftRows Explanation: This provides diffusion by cyclically shifting the bytes in each row left by 0,1,2,3 positions respectively. This ensures that bytes in each column come from different columns in the previous state.")
    print("Row 0: no shift")
    print("Row 1: left shift by 1")
    print("Row 2: left shift by 2")
    print("Row 3: left shift by 3")
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]

def inv_shift_rows(state):
    print("\nInvShiftRows Explanation: Inverse of ShiftRows, shifting right instead.")
    print("Row 0: no shift")
    print("Row 1: right shift by 1")
    print("Row 2: right shift by 2")
    print("Row 3: right shift by 3")
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]

def mix_columns(state):
    print("\nMixColumns Explanation: This linear transformation provides diffusion over columns. Each column is treated as a polynomial over GF(2^8) and multiplied by a fixed matrix:")
    print("[[2, 3, 1, 1],")
    print(" [1, 2, 3, 1],")
    print(" [1, 1, 2, 3],")
    print(" [3, 1, 1, 2]]")
    print("Multiplications use GF(2^8) arithmetic with irreducible polynomial x^8 + x^4 + x^3 + x + 1.")
    print("Example: For a column [a, b, c, d], new[0] = 2*a + 3*b + 1*c + 1*d (where + is XOR, * is gf_mult)")
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        print(f"\nProcessing Column {c}: {col[0]:02x} {col[1]:02x} {col[2]:02x} {col[3]:02x}")
        temp0 = gf_mult(2, col[0]) ^ gf_mult(3, col[1]) ^ col[2] ^ col[3]
        print(f"New byte 0: 2*{col[0]:02x}={gf_mult(2, col[0]):02x} ^ 3*{col[1]:02x}={gf_mult(3, col[1]):02x} ^ {col[2]:02x} ^ {col[3]:02x} = {temp0:02x}")
        temp1 = col[0] ^ gf_mult(2, col[1]) ^ gf_mult(3, col[2]) ^ col[3]
        print(f"New byte 1: {col[0]:02x} ^ 2*{col[1]:02x}={gf_mult(2, col[1]):02x} ^ 3*{col[2]:02x}={gf_mult(3, col[2]):02x} ^ {col[3]:02x} = {temp1:02x}")
        temp2 = col[0] ^ col[1] ^ gf_mult(2, col[2]) ^ gf_mult(3, col[3])
        print(f"New byte 2: {col[0]:02x} ^ {col[1]:02x} ^ 2*{col[2]:02x}={gf_mult(2, col[2]):02x} ^ 3*{col[3]:02x}={gf_mult(3, col[3]):02x} = {temp2:02x}")
        temp3 = gf_mult(3, col[0]) ^ col[1] ^ col[2] ^ gf_mult(2, col[3])
        print(f"New byte 3: 3*{col[0]:02x}={gf_mult(3, col[0]):02x} ^ {col[1]:02x} ^ {col[2]:02x} ^ 2*{col[3]:02x}={gf_mult(2, col[3]):02x} = {temp3:02x}")
        state[0][c] = temp0
        state[1][c] = temp1
        state[2][c] = temp2
        state[3][c] = temp3

def inv_mix_columns(state):
    print("\nInvMixColumns Explanation: Inverse of MixColumns, using the inverse matrix:")
    print("[[0xe, 0xb, 0xd, 0x9],")
    print(" [0x9, 0xe, 0xb, 0xd],")
    print(" [0xd, 0x9, 0xe, 0xb],")
    print(" [0xb, 0xd, 0x9, 0xe]]")
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        print(f"\nProcessing Column {c}: {col[0]:02x} {col[1]:02x} {col[2]:02x} {col[3]:02x}")
        temp0 = gf_mult(0x0e, col[0]) ^ gf_mult(0x0b, col[1]) ^ gf_mult(0x0d, col[2]) ^ gf_mult(0x09, col[3])
        print(f"New byte 0: 0e*{col[0]:02x}={gf_mult(0x0e, col[0]):02x} ^ 0b*{col[1]:02x}={gf_mult(0x0b, col[1]):02x} ^ 0d*{col[2]:02x}={gf_mult(0x0d, col[2]):02x} ^ 09*{col[3]:02x}={gf_mult(0x09, col[3]):02x} = {temp0:02x}")
        temp1 = gf_mult(0x09, col[0]) ^ gf_mult(0x0e, col[1]) ^ gf_mult(0x0b, col[2]) ^ gf_mult(0x0d, col[3])
        print(f"New byte 1: 09*{col[0]:02x}={gf_mult(0x09, col[0]):02x} ^ 0e*{col[1]:02x}={gf_mult(0x0e, col[1]):02x} ^ 0b*{col[2]:02x}={gf_mult(0x0b, col[2]):02x} ^ 0d*{col[3]:02x}={gf_mult(0x0d, col[3]):02x} = {temp1:02x}")
        temp2 = gf_mult(0x0d, col[0]) ^ gf_mult(0x09, col[1]) ^ gf_mult(0x0e, col[2]) ^ gf_mult(0x0b, col[3])
        print(f"New byte 2: 0d*{col[0]:02x}={gf_mult(0x0d, col[0]):02x} ^ 09*{col[1]:02x}={gf_mult(0x09, col[1]):02x} ^ 0e*{col[2]:02x}={gf_mult(0x0e, col[2]):02x} ^ 0b*{col[3]:02x}={gf_mult(0x0b, col[3]):02x} = {temp2:02x}")
        temp3 = gf_mult(0x0b, col[0]) ^ gf_mult(0x0d, col[1]) ^ gf_mult(0x09, col[2]) ^ gf_mult(0x0e, col[3])
        print(f"New byte 3: 0b*{col[0]:02x}={gf_mult(0x0b, col[0]):02x} ^ 0d*{col[1]:02x}={gf_mult(0x0d, col[1]):02x} ^ 09*{col[2]:02x}={gf_mult(0x09, col[2]):02x} ^ 0e*{col[3]:02x}={gf_mult(0x0e, col[3]):02x} = {temp3:02x}")
        state[0][c] = temp0
        state[1][c] = temp1
        state[2][c] = temp2
        state[3][c] = temp3

def add_round_key(state, round_key):
    print("\nAddRoundKey Explanation: This step combines the state with the round key using bitwise XOR. It introduces the secret key into the process at each round.")
    for r in range(4):
        for c in range(4):
            state[r][c] ^= round_key[r][c]

def verbose_key_expansion(key):
    print("\nKey Expansion Explanation: The 128-bit key is expanded into 11 round keys (one for each round plus initial). It uses 4-word (32-bit) units.")
    print("Operations: For each new word: If multiple of 4, apply RotWord (rotate left by 1 byte), SubWord (apply S-box to each byte), XOR with Rcon (round constant). Then XOR with word 4 positions earlier.")
    w = [0] * 44
    for i in range(4):
        w[i] = (key[4 * i] << 24) | (key[4 * i + 1] << 16) | (key[4 * i + 2] << 8) | key[4 * i + 3]
        print_word(f"Initial w[{i}]", w[i])
    
    for i in range(4, 44):
        clear_screen()
        print(f"\nGenerating w[{i}]")
        temp = w[i - 1]
        print_word("temp = w[i-1]", temp)
        if i % 4 == 0:
            # RotWord
            temp = ((temp << 8) | (temp >> 24)) & 0xffffffff
            print_word("After RotWord", temp)
            # SubWord
            temp = (sbox[(temp >> 24) & 0xff] << 24) | (sbox[(temp >> 16) & 0xff] << 16) | \
                   (sbox[(temp >> 8) & 0xff] << 8) | sbox[temp & 0xff]
            print_word("After SubWord", temp)
            # XOR with Rcon
            rc = rcon[(i // 4) - 1]
            print(f"Rcon[{ (i // 4) - 1 }] = {rc:02x} 00 00 00")
            temp ^= rc << 24
            print_word("After XOR Rcon", temp)
        print_word("w[i-4]", w[i - 4])
        w[i] = w[i - 4] ^ temp
        print_word(f"w[{i}] = w[i-4] ^ temp", w[i])
        input("Press Enter to continue...")
    
    round_keys = []
    for i in range(11):
        rk = [[0] * 4 for _ in range(4)]
        for j in range(4):
            word = w[4 * i + j]
            rk[0][j] = (word >> 24) & 0xff
            rk[1][j] = (word >> 16) & 0xff
            rk[2][j] = (word >> 8) & 0xff
            rk[3][j] = word & 0xff
        round_keys.append(rk)
    
    clear_screen()
    print("\nAll Round Keys:")
    for i in range(11):
        print(f"Round Key {i}:")
        print_state_diff("", round_keys[i])
        print()
    
    return round_keys

# Main demo

def main():
    clear_screen()
    print("\n=== AES-128 Step-by-Step Interactive Demonstration with Explanations ===\n")

    # Key Input
    user_key_str = input("Enter a key (16 chars for AES-128, will be padded/truncated): ")
    user_key = user_key_str.encode('utf-8')[:16].ljust(16, b'\0')
    print_bytes_hex("[1] Key (16 bytes)", user_key)

    # Plaintext Input
    plaintext_str = input("Enter plaintext: ")
    plaintext = plaintext_str.encode('utf-8')
    plaintext_padded = pad(plaintext)
    print_bytes_hex("[2] Plaintext (padded)", plaintext_padded)

    blocks = [plaintext_padded[i:i+16] for i in range(0, len(plaintext_padded), 16)]
    if len(blocks) > 1:
        print("Note: Detailed steps will be shown only for the first block.")
    first_block = blocks[0]

    # Key Expansion
    print("\n=== Key Expansion ===\n")
    round_keys = verbose_key_expansion(user_key)

    input("Press Enter to continue to encryption...")

    # Encryption
    print("\n=== Encryption Process (for first block) ===\n")
    state = bytes_to_state(first_block)
    print_state_diff("[Initial State]", state)

    print("\nInitial Round: AddRoundKey")
    prev_state = [row[:] for row in state]
    add_round_key(state, round_keys[0])
    print_state_diff("[After Initial AddRoundKey]", state, prev_state)
    input("Press Enter to continue...")

    for round_num in range(1, 11):
        clear_screen()
        print(f"\n=== Round {round_num} ===\n")

        prev_state = [row[:] for row in state]
        sub_bytes(state)
        print_state_diff("[After SubBytes]", state, prev_state)
        input("Press Enter to continue...")

        prev_state = [row[:] for row in state]
        shift_rows(state)
        print_state_diff("[After ShiftRows]", state, prev_state)
        input("Press Enter to continue...")

        if round_num < 10:
            prev_state = [row[:] for row in state]
            mix_columns(state)
            print_state_diff("[After MixColumns]", state, prev_state)
            input("Press Enter to continue...")

        prev_state = [row[:] for row in state]
        add_round_key(state, round_keys[round_num])
        print_state_diff("[After AddRoundKey]", state, prev_state)
        input("Press Enter to continue to next round..." if round_num < 10 else "Press Enter to see ciphertext...")

    cipher_block = state_to_bytes(state)
    ciphertext = cipher_block
    if len(blocks) > 1:
        ciphertext = b''
        for block in blocks:
            state = bytes_to_state(block)
            add_round_key(state, round_keys[0])
            for r in range(1, 10):
                sub_bytes(state)
                shift_rows(state)
                mix_columns(state)
                add_round_key(state, round_keys[r])
            sub_bytes(state)
            shift_rows(state)
            add_round_key(state, round_keys[10])
            ciphertext += state_to_bytes(state)

    print_bytes_hex("[3] Ciphertext", ciphertext)

    input("Press Enter to continue to decryption...")

    # Decryption
    print("\n=== Decryption Process (for first block) ===\n")
    state = bytes_to_state(cipher_block if len(blocks) == 1 else ciphertext[:16])
    print_state_diff("[Ciphertext State]", state)

    print("\nInitial Round: AddRoundKey with Round Key 10")
    prev_state = [row[:] for row in state]
    add_round_key(state, round_keys[10])
    print_state_diff("[After Initial AddRoundKey]", state, prev_state)
    input("Press Enter to continue...")

    for round_num in range(9, 0, -1):
        clear_screen()
        print(f"\n=== Inverse Round (corresponding to encryption round {11 - round_num}) ===\n")

        prev_state = [row[:] for row in state]
        inv_shift_rows(state)
        print_state_diff("[After InvShiftRows]", state, prev_state)
        input("Press Enter to continue...")

        prev_state = [row[:] for row in state]
        inv_sub_bytes(state)
        print_state_diff("[After InvSubBytes]", state, prev_state)
        input("Press Enter to continue...")

        prev_state = [row[:] for row in state]
        add_round_key(state, round_keys[round_num])
        print_state_diff("[After AddRoundKey]", state, prev_state)
        input("Press Enter to continue...")

        prev_state = [row[:] for row in state]
        inv_mix_columns(state)
        print_state_diff("[After InvMixColumns]", state, prev_state)
        input("Press Enter to continue to next inverse round...")

    clear_screen()
    print("\n=== Final Inverse Round ===\n")

    prev_state = [row[:] for row in state]
    inv_shift_rows(state)
    print_state_diff("[After InvShiftRows]", state, prev_state)
    input("Press Enter to continue...")

    prev_state = [row[:] for row in state]
    inv_sub_bytes(state)
    print_state_diff("[After InvSubBytes]", state, prev_state)
    input("Press Enter to continue...")

    prev_state = [row[:] for row in state]
    add_round_key(state, round_keys[0])
    print_state_diff("[After AddRoundKey]", state, prev_state)
    input("Press Enter to see decrypted text...")

    decrypted_padded_block = state_to_bytes(state)
    decrypted_padded = decrypted_padded_block
    if len(blocks) > 1:
        decrypted_padded = b''
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            state = bytes_to_state(block)
            add_round_key(state, round_keys[10])
            for r in range(9, 0, -1):
                inv_shift_rows(state)
                inv_sub_bytes(state)
                add_round_key(state, round_keys[r])
                inv_mix_columns(state)
            inv_shift_rows(state)
            inv_sub_bytes(state)
            add_round_key(state, round_keys[0])
            decrypted_padded += state_to_bytes(state)

    decrypted = unpad(decrypted_padded)
    print_bytes_hex("[4] Decrypted (padded)", decrypted_padded)
    print("[5] Decrypted plaintext:", decrypted.decode(errors='ignore'))

    print("\n=== AES-128 Demonstration Complete ===")

if __name__ == "__main__":
    main()