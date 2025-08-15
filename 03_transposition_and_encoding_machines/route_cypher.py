#!/usr/bin/env python3
"""
Route Cipher (Transposition Cipher) Educational Demo
A didactical script with animated visualization to demonstrate how route ciphers work step by step
"""

import time
import os
import sys

def print_header():
    print("=" * 60)
    print("    ROUTE CIPHER (TRANSPOSITION CIPHER) DEMONSTRATION")
    print("=" * 60)
    print()

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_animated_grid(grid, current_pos=None, collected_chars="", title="Grid Animation", delay=0.8):
    """Print grid with current position highlighted and collected characters shown"""
    rows, cols = len(grid), len(grid[0])
    
    print(f"\n{title}")
    print(f"Collected so far: [{collected_chars}]")
    print("+" + "━" * (cols * 4 - 1) + "+")
    
    for row in range(rows):
        print("│", end="")
        for col in range(cols):
            if current_pos and (row, col) == current_pos:
                # Highlight current position with arrow
                print(f"→{grid[row][col]}←", end="│")
            else:
                print(f" {grid[row][col]} ", end="│")
        print()
    
    print("+" + "━" * (cols * 4 - 1) + "+")
    
    if current_pos:
        row, col = current_pos
        print(f"Reading position: Row {row+1}, Column {col+1} → '{grid[row][col]}'")
    
    time.sleep(delay)

def create_grid(text, rows, cols):
    """Create a grid from text, padding with 'X' if necessary"""
    # Remove spaces and convert to uppercase
    text = text.replace(" ", "").upper()
    
    # Calculate required padding
    total_cells = rows * cols
    padding_needed = total_cells - len(text)
    
    if padding_needed > 0:
        text += 'X' * padding_needed
        print(f"Text padded with {padding_needed} 'X' characters to fill the grid")
    
    # Create 2D grid
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            index = i * cols + j
            if index < len(text):
                row.append(text[index])
            else:
                row.append('X')
        grid.append(row)
    
    return grid, text

def print_step(step_num, description):
    print(f"STEP {step_num}: {description}")
    print("-" * 50)

def animate_reading_pattern(grid, path, pattern_name, speed="normal"):
    """Animate the reading pattern with arrows showing the path"""
    speeds = {"slow": 1.2, "normal": 0.8, "fast": 0.4}
    delay = speeds.get(speed, 0.8)
    
    print(f"\n🎬 ANIMATED DEMONSTRATION: {pattern_name}")
    print("=" * 60)
    print("Watch the arrow (→←) move through the grid following the pattern!")
    print("Press Ctrl+C at any time to skip animation\n")
    
    input("Press Enter to start the animation...")
    
    try:
        collected = ""
        for i, (row, col) in enumerate(path):
            clear_screen()
            collected += grid[row][col]
            
            print(f"🔄 Step {i+1} of {len(path)}")
            print_animated_grid(grid, (row, col), collected, 
                              f"Reading with {pattern_name}", delay)
            
            # Add directional indicators for next move if not last step
            if i < len(path) - 1:
                next_row, next_col = path[i + 1]
                direction = get_direction_arrow(row, col, next_row, next_col)
                print(f"Next move: {direction}")
        
        # Final result
        clear_screen()
        print(f"✅ ANIMATION COMPLETE!")
        print(f"Pattern: {pattern_name}")
        print_animated_grid(grid, None, collected, "Final Result", 0)
        print(f"🔐 Encrypted text: {collected}")
        print("\nAnimation finished! The cipher text is now complete.")
        
    except KeyboardInterrupt:
        print(f"\n⏭️  Animation skipped. Final result: {collected}")
    
    input("\nPress Enter to continue...")
    return collected

def get_direction_arrow(curr_row, curr_col, next_row, next_col):
    """Get directional arrow for next move"""
    if next_row == curr_row:
        if next_col > curr_col:
            return "➡️  Moving RIGHT"
        else:
            return "⬅️  Moving LEFT"
    elif next_col == curr_col:
        if next_row > curr_row:
            return "⬇️  Moving DOWN"
        else:
            return "⬆️  Moving UP"
    elif next_row > curr_row and next_col > curr_col:
        return "↘️  Moving DIAGONAL DOWN-RIGHT"
    elif next_row > curr_row and next_col < curr_col:
        return "↙️  Moving DIAGONAL DOWN-LEFT"
    elif next_row < curr_row and next_col > curr_col:
        return "↗️  Moving DIAGONAL UP-RIGHT"
    else:
        return "↖️  Moving DIAGONAL UP-LEFT"
def print_grid(grid, title="Grid"):
    """Print a static grid"""
    print(f"\n{title}:")
    print("+" + "-" * (len(grid[0]) * 4 - 1) + "+")
    for row in grid:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "-" * (len(grid[0]) * 4 - 1) + "+")
    print()

def demonstrate_basic_concept():
    print_step(1, "Understanding Route Cipher Basics")
    print("A route cipher rearranges letters by:")
    print("1. Writing the message in a rectangular grid")
    print("2. Reading the letters following a specific pattern/route")
    print("3. The 'key' is the dimensions and reading pattern\n")
    
    # Simple example
    message = "HELLO WORLD"
    print(f"Example message: '{message}'")
    
    rows, cols = 3, 4
    grid, padded_text = create_grid(message, rows, cols)
    
    print(f"Grid dimensions: {rows} rows × {cols} columns")
    print_grid(grid, "Message written row by row")
    
    # Read column by column
    cipher_text = ""
    for col in range(cols):
        for row in range(rows):
            cipher_text += grid[row][col]
    
    print(f"Reading column by column: {cipher_text}")
    print(f"Encrypted message: {cipher_text}\n")

def get_route_patterns():
    """Return available route patterns with descriptions"""
    patterns = {
        "1": {
            "name": "Column-wise (top to bottom)",
            "description": "Read each column from top to bottom, left to right",
            "function": read_column_wise
        },
        "2": {
            "name": "Row-wise (left to right)", 
            "description": "Read each row from left to right, top to bottom",
            "function": read_row_wise
        },
        "3": {
            "name": "Diagonal (top-left to bottom-right)",
            "description": "Read diagonally from top-left to bottom-right",
            "function": read_diagonal
        },
        "4": {
            "name": "Spiral (clockwise from outside)",
            "description": "Read in a clockwise spiral from the outside",
            "function": read_spiral_clockwise
        },
        "5": {
            "name": "Snake/Boustrophedon",
            "description": "Read left-to-right, then right-to-left alternating",
            "function": read_snake
        }
    }
    return patterns

def read_column_wise(grid):
    """Read grid column by column, top to bottom"""
    result = ""
    path = []
    for col in range(len(grid[0])):
        for row in range(len(grid)):
            result += grid[row][col]
            path.append((row, col))
    return result, path

def read_row_wise(grid):
    """Read grid row by row, left to right"""
    result = ""
    path = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            result += grid[row][col]
            path.append((row, col))
    return result, path

def read_diagonal(grid):
    """Read grid diagonally"""
    result = ""
    path = []
    rows, cols = len(grid), len(grid[0])
    
    # Start from top-left, read main diagonal and parallel diagonals
    for start_col in range(cols):
        row, col = 0, start_col
        while row < rows and col < cols:
            result += grid[row][col]
            path.append((row, col))
            row += 1
            col += 1
    
    for start_row in range(1, rows):
        row, col = start_row, 0
        while row < rows and col < cols:
            result += grid[row][col]
            path.append((row, col))
            row += 1
            col += 1
    
    return result, path

def read_spiral_clockwise(grid):
    """Read grid in clockwise spiral from outside"""
    if not grid:
        return "", []
    
    result = ""
    path = []
    rows, cols = len(grid), len(grid[0])
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right:
        # Read top row
        for col in range(left, right + 1):
            result += grid[top][col]
            path.append((top, col))
        top += 1
        
        # Read right column
        for row in range(top, bottom + 1):
            result += grid[row][right]
            path.append((row, right))
        right -= 1
        
        # Read bottom row (if exists)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result += grid[bottom][col]
                path.append((bottom, col))
            bottom -= 1
        
        # Read left column (if exists)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result += grid[row][left]
                path.append((row, left))
            left += 1
    
    return result, path

def read_snake(grid):
    """Read in snake pattern (boustrophedon)"""
    result = ""
    path = []
    rows, cols = len(grid), len(grid[0])
    
    for row in range(rows):
        if row % 2 == 0:  # Even rows: left to right
            for col in range(cols):
                result += grid[row][col]
                path.append((row, col))
        else:  # Odd rows: right to left
            for col in range(cols - 1, -1, -1):
                result += grid[row][col]
                path.append((row, col))
    
    return result, path

def visualize_path(grid, path, pattern_name):
    """Show the reading path with numbers"""
    rows, cols = len(grid), len(grid[0])
    path_grid = [["  " for _ in range(cols)] for _ in range(rows)]
    
    for i, (row, col) in enumerate(path):
        path_grid[row][col] = f"{i+1:2d}"
    
    print(f"\nReading order for {pattern_name}:")
    print("+" + "-" * (cols * 4 - 1) + "+")
    for row in path_grid:
        print("|", end="")
        for cell in row:
            print(f"{cell}|", end="")
        print()
    print("+" + "-" * (cols * 4 - 1) + "+")

def generate_key_explanation(rows, cols, pattern_name, cipher_text):
    """Generate explanation of the key"""
    print(f"\nKEY EXPLANATION:")
    print("=" * 40)
    print(f"Grid Dimensions: {rows} rows × {cols} columns")
    print(f"Reading Pattern: {pattern_name}")
    print(f"Key can be written as: ({rows}, {cols}, '{pattern_name}')")
    print(f"Result: {cipher_text}")
    print("=" * 40)

def interactive_demo():
    print_step(2, "Interactive Route Cipher Demo")
    
    # Get message from user
    while True:
        message = input("Enter your message to encrypt: ").strip()
        if message:
            break
        print("Please enter a non-empty message.")
    
    # Get grid dimensions
    while True:
        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            if rows > 0 and cols > 0:
                break
            print("Rows and columns must be positive numbers.")
        except ValueError:
            print("Please enter valid numbers.")
    
    # Show available patterns
    patterns = get_route_patterns()
    print(f"\nAvailable reading patterns:")
    for key, pattern in patterns.items():
        print(f"{key}. {pattern['name']} - {pattern['description']}")
    
    # Get pattern choice
    while True:
        choice = input(f"\nChoose a pattern (1-{len(patterns)}): ").strip()
        if choice in patterns:
            break
        print(f"Please choose a number between 1 and {len(patterns)}.")
    
    selected_pattern = patterns[choice]
    
    # Get animation speed preference
    print(f"\nAnimation speeds:")
    print("1. Slow (1.2s per step) - Good for detailed observation")
    print("2. Normal (0.8s per step) - Recommended")
    print("3. Fast (0.4s per step) - Quick overview")
    
    speed_choice = input("Choose animation speed (1-3, default 2): ").strip()
    speed_map = {"1": "slow", "2": "normal", "3": "fast"}
    speed = speed_map.get(speed_choice, "normal")
    
    # Process the encryption
    print(f"\nProcessing encryption with {selected_pattern['name']}...")
    print("=" * 60)
    
    # Create and display grid
    grid, padded_text = create_grid(message, rows, cols)
    print(f"Original message: '{message}'")
    print(f"Padded text: '{padded_text}'")
    print_grid(grid, "Message placed in grid")
    
    input("Press Enter to start the animated encryption process...")
    
    # Apply the chosen pattern with animation
    _, path = selected_pattern['function'](grid)
    cipher_text = animate_reading_pattern(grid, path, selected_pattern['name'], speed)
    
    # Show the final results
    clear_screen()
    print("🎉 ENCRYPTION COMPLETE!")
    print("=" * 60)
    
    # Show the reading path visualization
    visualize_path(grid, path, selected_pattern['name'])
    
    # Generate key explanation
    generate_key_explanation(rows, cols, selected_pattern['name'], cipher_text)
    
    return cipher_text, (rows, cols, selected_pattern['name'])

def demonstrate_decryption():
    print_step(3, "Decryption Process")
    print("To decrypt a route cipher:")
    print("1. You need the same grid dimensions")
    print("2. You need to know the reading pattern used")
    print("3. Create the grid and fill it using the SAME pattern")
    print("4. Read the message row by row to get the original text")
    print()
    
    cipher = input("Enter cipher text to decrypt: ").strip().upper()
    
    while True:
        try:
            rows = int(input("Enter number of rows used: "))
            cols = int(input("Enter number of columns used: "))
            if rows > 0 and cols > 0 and len(cipher) <= rows * cols:
                break
            print("Invalid dimensions or cipher text too long for grid.")
        except ValueError:
            print("Please enter valid numbers.")
    
    # Show available patterns for decryption
    patterns = get_route_patterns()
    print(f"\nWhich reading pattern was used for encryption?")
    for key, pattern in patterns.items():
        print(f"{key}. {pattern['name']}")
    
    while True:
        choice = input(f"\nChoose the pattern that was used (1-{len(patterns)}): ").strip()
        if choice in patterns:
            break
        print(f"Please choose a number between 1 and {len(patterns)}.")
    
    selected_pattern = patterns[choice]
    
    # Show how to reconstruct with the correct pattern
    print(f"\n🔄 DECRYPTION ANIMATION using {selected_pattern['name']}")
    input("Press Enter to watch the decryption process...")
    
    # Create empty grid
    grid = [["?" for _ in range(cols)] for _ in range(rows)]
    
    # Get the reading path for the selected pattern
    temp_grid = [["X" for _ in range(cols)] for _ in range(rows)]
    _, path = selected_pattern['function'](temp_grid)
    
    try:
        # Fill the grid using the same pattern that was used for encryption
        for i, (row, col) in enumerate(path):
            if i < len(cipher):
                clear_screen()
                grid[row][col] = cipher[i]
                print(f"🔓 Decryption Step {i + 1}")
                print(f"Placing '{cipher[i]}' at position ({row+1}, {col+1})")
                print(f"Following {selected_pattern['name']} pattern")
                print_animated_grid(grid, (row, col), "", "Reconstructing Grid", 0.6)
    except KeyboardInterrupt:
        print("Animation skipped.")
    
    clear_screen()
    print_grid(grid, f"Grid reconstructed using {selected_pattern['name']}")
    
    # Read row by row to get original message
    print("Now reading the grid row by row to get the original message...")
    decrypted = ""
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "?":
                decrypted += grid[row][col]
    
    # Remove padding X's from the end
    decrypted = decrypted.rstrip('X')
    print(f"✅ Decrypted message: '{decrypted}'")
    
    # Show the reading order for clarity
    print(f"\n💡 Key insight: We filled the grid using the {selected_pattern['name']} pattern,")
    print("then read row by row to recover the original message!")

def demonstrate_full_cycle():
    """Demonstrate a complete encrypt-decrypt cycle"""
    print_step(4, "Complete Encryption-Decryption Cycle")
    print("Let's do a complete cycle to verify our understanding!")
    print()
    
    # Simple example for verification
    message = "CRYPTOGRAPHY"
    rows, cols = 3, 4
    pattern_choice = "4"  # Spiral clockwise
    
    patterns = get_route_patterns()
    selected_pattern = patterns[pattern_choice]
    
    print(f"Test message: '{message}'")
    print(f"Grid: {rows}×{cols}")
    print(f"Pattern: {selected_pattern['name']}")
    
    # Encrypt
    grid, padded_text = create_grid(message, rows, cols)
    print_grid(grid, "Original grid (row by row)")
    
    cipher_text, path = selected_pattern['function'](grid)
    print(f"Encrypted: {cipher_text}")
    
    # Decrypt
    print(f"\nNow decrypting '{cipher_text}'...")
    decrypt_grid = [["" for _ in range(cols)] for _ in range(rows)]
    
    # Fill using the same pattern
    for i, (row, col) in enumerate(path):
        if i < len(cipher_text):
            decrypt_grid[row][col] = cipher_text[i]
    
    print_grid(decrypt_grid, "Reconstructed grid")
    
    # Read row by row
    decrypted = ""
    for row in range(rows):
        for col in range(cols):
            decrypted += decrypt_grid[row][col]
    
    decrypted = decrypted.rstrip('X')
    print(f"Decrypted: '{decrypted}'")
    print(f"Original:  '{message}'")
    print(f"Match: {'✅ YES' if decrypted == message else '❌ NO'}")

def main():
    print_header()
    
    # Ask if user wants to see basic demo
    show_basic = input("Show basic demonstration first? (y/n, default y): ").strip().lower()
    if show_basic != 'n':
        demonstrate_basic_concept()
        input("Press Enter to continue to interactive demo...")
    
    print("\n" + "=" * 60)
    
    # Interactive demo
    cipher_result, key_info = interactive_demo()
    
    print("\n" + "=" * 60)
    show_decrypt = input("Show decryption demonstration? (y/n, default y): ").strip().lower()
    if show_decrypt != 'n':
        demonstrate_decryption()
    
    print("\n" + "=" * 60)
    show_cycle = input("Show complete encryption-decryption cycle? (y/n, default y): ").strip().lower()
    if show_cycle != 'n':
        demonstrate_full_cycle()
    
    print(f"\n{'='*60}")
    print("📚 EDUCATIONAL SUMMARY:")
    print("• Route ciphers are transposition ciphers that rearrange letters")
    print("• The animation shows how patterns create different cipher texts")
    print("• CRITICAL: Decryption must use the SAME pattern as encryption!")
    print("• Security depends on keeping the grid dimensions and pattern secret")
    print("• Easy to implement but vulnerable to frequency analysis")
    print("• Perfect for understanding basic cryptography concepts!")
    print("• Try different patterns to see how they affect the result!")
    print("="*60)

if __name__ == "__main__":
    main()
