import itertools
import math
import re

# -----------------------------
# Helpers
# -----------------------------

def score_english(text):
    """Basic scoring function: counts dictionary word hits."""
    common_words = ["THE", "AND", "WE", "ARE", "OF", "TO", "IN", "FLEE", "DISCOVERED", "ONCE"]
    return sum(text.count(w) for w in common_words)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# -----------------------------
# Rail Fence Cipher
# -----------------------------
def rail_fence_decrypt(ciphertext, rails):
    """Decrypt a rail fence cipher with given number of rails."""
    length = len(ciphertext)
    fence = [[None] * length for _ in range(rails)]
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    pattern = pattern * (length // len(pattern) + 1)
    # Place markers
    idx = 0
    for r in range(rails):
        for i in range(length):
            if pattern[i] == r:
                fence[r][i] = '*'
    # Fill in ciphertext
    it = iter(ciphertext)
    for r in range(rails):
        for i in range(length):
            if fence[r][i] == '*':
                fence[r][i] = next(it)
    # Read in zig-zag
    result = []
    for i in range(length):
        r = pattern[i]
        result.append(fence[r][i])
    return ''.join(result)

# -----------------------------
# Columnar Transposition
# -----------------------------
def columnar_decrypt(ciphertext, key_order):
    """Decrypt a columnar transposition given key order (list of column indices)."""
    cols = len(key_order)
    rows = math.ceil(len(ciphertext) / cols)
    # Fill columns in key order
    grid = [''] * cols
    pos = 0
    for k in sorted(range(cols), key=lambda x: key_order[x]):
        l = rows
        if k >= len(ciphertext) % cols and len(ciphertext) % cols != 0:
            l -= 1
        grid[k] = list(ciphertext[pos:pos+l])
        pos += l
    # Read row-wise
    plaintext = ''
    for r in range(rows):
        for c in range(cols):
            if r < len(grid[c]):
                plaintext += grid[c][r]
    return plaintext

# -----------------------------
# Myszkowski Transposition
# -----------------------------
def myszkowski_decrypt(ciphertext, key):
    """Decrypt Myszkowski transposition with given key string."""
    key_nums = []
    sorted_key = sorted(set(key), key=lambda k: (key.index(k)))
    mapping = {ch: idx for idx, ch in enumerate(sorted_key)}
    for ch in key:
        key_nums.append(mapping[ch])
    unique_vals = sorted(set(key_nums))
    cols = len(key)
    rows = math.ceil(len(ciphertext) / cols)
    grid = [[''] * cols for _ in range(rows)]
    pos = 0
    for val in unique_vals:
        indices = [i for i, v in enumerate(key_nums) if v == val]
        for i in indices:
            for r in range(rows):
                if pos < len(ciphertext):
                    grid[r][i] = ciphertext[pos]
                    pos += 1
    return ''.join(''.join(row) for row in grid)

# -----------------------------
# Double Transposition
# -----------------------------
def double_transposition_decrypt(ciphertext, key1, key2):
    pt = columnar_decrypt(ciphertext, key1)
    pt = columnar_decrypt(pt, key2)
    return pt

# -----------------------------
# Route Cipher
# -----------------------------
def spiral_coords(rows, cols):
    """Generate coordinates for spiral reading order."""
    coords = []
    top, left = 0, 0
    bottom, right = rows - 1, cols - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            coords.append((top, c))
        top += 1
        for r in range(top, bottom + 1):
            coords.append((r, right))
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                coords.append((bottom, c))
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                coords.append((r, left))
            left += 1
    return coords

def route_decrypt(ciphertext, rows, cols, coords):
    grid = [[''] * cols for _ in range(rows)]
    pos = 0
    for r in range(rows):
        for c in range(cols):
            grid[r][c] = ciphertext[pos]
            pos += 1
    return ''.join(grid[r][c] for r, c in coords)

# -----------------------------
# Brute Force
# -----------------------------
def brute_force_transpositions(ciphertext):
    results = []
    
    # Rail Fence
    for rails in range(2, min(10, len(ciphertext)//2)):
        pt = rail_fence_decrypt(ciphertext, rails)
        results.append(("Rail Fence", rails, pt, score_english(pt)))
    
    # Columnar (try small key lengths)
    for cols in range(2, 7):
        for key_order in itertools.permutations(range(cols)):
            pt = columnar_decrypt(ciphertext, list(key_order))
            results.append(("Columnar", key_order, pt, score_english(pt)))
    
    # Route Cipher (spiral)
    for rows in range(2, len(ciphertext)//2):
        if len(ciphertext) % rows == 0:
            cols = len(ciphertext) // rows
            coords = spiral_coords(rows, cols)
            pt = route_decrypt(ciphertext, rows, cols, coords)
            results.append(("Route Cipher Spiral", (rows, cols), pt, score_english(pt)))
    
    # Sort by score
    results.sort(key=lambda x: x[3], reverse=True)
    return results[:10]

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    CIPHERTEXT = "WEAREOCECNTOFLTEEEARDIVEDS"
    top_results = brute_force_transpositions(CIPHERTEXT)
    for method, key, pt, score in top_results:
        print(f"[{method}] Key: {key} | Score: {score} | PT: {pt}")
