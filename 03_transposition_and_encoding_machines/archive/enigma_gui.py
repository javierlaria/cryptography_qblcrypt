import tkinter as tk
from tkinter import messagebox, ttk
import math

# Constants and mapping definitions
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2I = {c: i for i, c in enumerate(ALPHABET)}
I2A = {i: c for c, i in A2I.items()}

# Historical rotor wirings and notch positions
ROTOR_SPECS = {
    "I":  {"wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": "Q"},
    "II": {"wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": "E"},
    "III":{"wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": "V"},
    "IV": {"wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": "J"},
    "V":  {"wiring": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": "Z"},
}

# Reflectors
REFLECTOR_SPECS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

def sanitize_plugboard_input(s: str):
    """Parse a plugboard specification like 'AB CD EF' into [('A','B'), ('C','D'), ...]"""
    parts = s.strip().upper().split()
    pairs = []
    used = set()
    for token in parts:
        token = token.strip()
        if len(token) == 2 and token[0] in ALPHABET and token[1] in ALPHABET:
            a, b = token[0], token[1]
            if a == b:
                continue
            if a in used or b in used:
                raise ValueError(f"Plugboard letter repeated: {a} or {b} already used.")
            pairs.append((a, b))
            used.add(a); used.add(b)
        else:
            raise ValueError(f"Invalid plugboard token: '{token}'. Use pairs like 'AB CD EF'.")
    if len(pairs) > 10:
        raise ValueError("At most 10 plugboard pairs are allowed.")
    return pairs

class Rotor:
    def __init__(self, name: str, wiring: str, notch: str, ring_setting: int = 1, position: str = "A"):
        self.name = name
        self.wiring = wiring.upper()
        self.notch = notch.upper()
        if not (1 <= ring_setting <= 26):
            raise ValueError("ring_setting must be in 1..26")
        self.ring = (ring_setting - 1)  # internal numeric 0..25
        if position not in ALPHABET:
            raise ValueError("position must be A-Z")
        self.pos = A2I[position]  # current rotor position 0..25
        # Precompute forward and backward mapping arrays (0..25)
        self.forward_map = [A2I[c] for c in self.wiring]
        # Build reverse mapping
        self.backward_map = [0] * 26
        for i, v in enumerate(self.forward_map):
            self.backward_map[v] = i

    def at_notch(self) -> bool:
        return I2A[self.pos] == self.notch

    def step(self):
        self.pos = (self.pos + 1) % 26

    def encode_forward(self, c_idx: int):
        rotor_coord = (c_idx + self.pos - self.ring) % 26
        mapped = self.forward_map[rotor_coord]
        out_idx = (mapped - self.pos + self.ring) % 26
        return out_idx

    def encode_backward(self, c_idx: int):
        rotor_coord = (c_idx + self.pos - self.ring) % 26
        mapped = self.backward_map[rotor_coord]
        out_idx = (mapped - self.pos + self.ring) % 26
        return out_idx

class EnigmaMachine:
    def __init__(self, rotor_names, ring_settings, initial_positions, reflector_name, plug_pairs):
        if len(rotor_names) != 3 or len(ring_settings) != 3 or len(initial_positions) != 3:
            raise ValueError("Provide exactly three rotors, three ring settings, three initial positions.")

        self.left = Rotor(rotor_names[0], ROTOR_SPECS[rotor_names[0]]["wiring"],
                          ROTOR_SPECS[rotor_names[0]]["notch"],
                          ring_settings[0], initial_positions[0])
        self.middle = Rotor(rotor_names[1], ROTOR_SPECS[rotor_names[1]]["wiring"],
                            ROTOR_SPECS[rotor_names[1]]["notch"],
                            ring_settings[1], initial_positions[1])
        self.right = Rotor(rotor_names[2], ROTOR_SPECS[rotor_names[2]]["wiring"],
                           ROTOR_SPECS[rotor_names[2]]["notch"],
                           ring_settings[2], initial_positions[2])

        if reflector_name not in REFLECTOR_SPECS:
            raise ValueError("Unsupported reflector. Choose 'B' or 'C'.")
        self.reflector_name = reflector_name
        self.reflector_wiring = [A2I[c] for c in REFLECTOR_SPECS[reflector_name]]

        self.plugboard = {c: c for c in ALPHABET}  # identity mapping initially
        for a, b in plug_pairs:
            self.plugboard[a] = b
            self.plugboard[b] = a

        self.initial_positions = [initial_positions[0], initial_positions[1], initial_positions[2]]

    def reset(self):
        self.left.pos = A2I[self.initial_positions[0]]
        self.middle.pos = A2I[self.initial_positions[1]]
        self.right.pos = A2I[self.initial_positions[2]]

    def plugboard_swap(self, letter: str):
        return self.plugboard.get(letter, letter)

    def reflector_map(self, idx: int):
        return self.reflector_wiring[idx]

    def step_rotors(self):
        middle_notch = self.middle.at_notch()
        right_notch = self.right.at_notch()

        if middle_notch:
            self.middle.step()
            self.left.step()
        if right_notch:
            self.middle.step()
        self.right.step()

    def encode_character(self, ch: str):
        ch = ch.upper()
        if ch not in ALPHABET:
            raise ValueError("Only A-Z letters allowed for encode_character.")

        self.step_rotors()

        swapped_in = self.plugboard_swap(ch)
        idx = A2I[swapped_in]
        right_out_idx = self.right.encode_forward(idx)
        right_out_letter = I2A[right_out_idx]
        idx = right_out_idx
        middle_out_idx = self.middle.encode_forward(idx)
        middle_out_letter = I2A[middle_out_idx]
        idx = middle_out_idx
        left_out_idx = self.left.encode_forward(idx)
        left_out_letter = I2A[left_out_idx]
        idx = left_out_idx
        refl_out_idx = self.reflector_map(idx)
        refl_out_letter = I2A[refl_out_idx]
        idx = refl_out_idx
        left_back_idx = self.left.encode_backward(idx)
        left_back_out_letter = I2A[left_back_idx]
        idx = left_back_idx
        middle_back_idx = self.middle.encode_backward(idx)
        middle_back_out_letter = I2A[middle_back_idx]
        idx = middle_back_idx
        right_back_idx = self.right.encode_backward(idx)
        right_back_out_letter = I2A[right_back_idx]
        out_letter = I2A[right_back_idx]
        swapped_out = self.plugboard_swap(out_letter)

        path_dict = {
            'input': ch,
            'plug_in_out': swapped_in,
            'right_out': right_out_letter,
            'middle_out': middle_out_letter,
            'left_out': left_out_letter,
            'refl_out': refl_out_letter,
            'left_back_out': left_back_out_letter,
            'middle_back_out': middle_back_out_letter,
            'right_back_out': right_back_out_letter,
            'plug_out_out': swapped_out,
        }
        return swapped_out, path_dict

    def status(self):
        lines = [
            f"Rotors (left->right): {self.left.name} {self.middle.name} {self.right.name}",
            f"Positions: Left={I2A[self.left.pos]} Middle={I2A[self.middle.pos]} Right={I2A[self.right.pos]}",
            f"Ring settings: Left={self.left.ring+1} Middle={self.middle.ring+1} Right={self.right.ring+1}",
            f"Reflector: {self.reflector_name}",
            f"Plugboard pairs: {', '.join([f'{a}{b}' for a,b in self._plug_pairs_list()])}"
        ]
        return lines

    def _plug_pairs_list(self):
        seen = set()
        pairs = []
        for c in ALPHABET:
            mapped = self.plugboard[c]
            if mapped != c and c not in seen:
                pairs.append((c, mapped))
                seen.add(c); seen.add(mapped)
        return pairs

class EnigmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enigma Machine Emulator")

        # Variables for configuration
        self.rotor_names = tk.StringVar(value="II I III")
        self.ring_settings = tk.StringVar(value="1 1 1")
        self.initial_positions = tk.StringVar(value="A A A")
        self.reflector_name = tk.StringVar(value="B")
        self.plug_pairs = tk.StringVar(value="")

        self.input_var = tk.StringVar(value="")
        self.encoded_var = tk.StringVar(value="")

        self.left_pos_var = tk.StringVar(value="A")
        self.middle_pos_var = tk.StringVar(value="A")
        self.right_pos_var = tk.StringVar(value="A")

        self.colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan', 'magenta']
        self.color_index = 0

        self.setup_gui()

        self.base_y = 50
        self.spacing = 22  # Increased spacing for better readability

        self.component_positions = {
            'keyboard': 40,
            'plugboard': 100,
            'right_entry': 180,
            'right_exit': 230,
            'middle_entry': 280,
            'middle_exit': 330,
            'left_entry': 380,
            'left_exit': 430,
            'reflector': 500,
        }

        self.enigma_machine = None
        self.setup_machine()

        self.root.bind('<Key>', self.on_key_press)

    def setup_gui(self):
        # Frame for configuration
        config_frame = ttk.LabelFrame(self.root, text="Machine Configuration")
        config_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Rotor selection
        ttk.Label(config_frame, text="Rotors (left middle right):").grid(row=0, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.rotor_names).grid(row=0, column=1, sticky="ew")

        # Ring settings
        ttk.Label(config_frame, text="Ring settings:").grid(row=1, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.ring_settings).grid(row=1, column=1, sticky="ew")

        # Initial positions
        ttk.Label(config_frame, text="Initial positions:").grid(row=2, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.initial_positions).grid(row=2, column=1, sticky="ew")

        # Reflector
        ttk.Label(config_frame, text="Reflector:").grid(row=3, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.reflector_name).grid(row=3, column=1, sticky="ew")

        # Plugboard
        ttk.Label(config_frame, text="Plugboard pairs:").grid(row=4, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.plug_pairs).grid(row=4, column=1, sticky="ew")

        # Setup button
        ttk.Button(config_frame, text="Setup Machine", command=self.setup_machine).grid(row=5, column=0, columnspan=2, pady=5)

        # Frame for encoding
        encode_frame = ttk.LabelFrame(self.root, text="Encode Message")
        encode_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Input display
        ttk.Label(encode_frame, text="Input:").grid(row=0, column=0, sticky="w")
        self.input_entry = ttk.Entry(encode_frame, textvariable=self.input_var, state='disabled')
        self.input_entry.grid(row=0, column=1, sticky="ew")

        # Encoded display
        ttk.Label(encode_frame, text="Encoded:").grid(row=1, column=0, sticky="w")
        self.encoded_entry = ttk.Entry(encode_frame, textvariable=self.encoded_var, state='disabled')
        self.encoded_entry.grid(row=1, column=1, sticky="ew")

        # Reset button
        ttk.Button(encode_frame, text="Reset", command=self.reset_machine).grid(row=2, column=0, columnspan=2, pady=5)

        # Note
        ttk.Label(encode_frame, text="Type A-Z keys to encode letters.").grid(row=3, column=0, columnspan=2)

        # Rotor positions display
        pos_frame = ttk.LabelFrame(self.root, text="Current Positions")
        pos_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(pos_frame, text="Left:").grid(row=0, column=0)
        ttk.Label(pos_frame, textvariable=self.left_pos_var).grid(row=0, column=1)
        ttk.Label(pos_frame, text="Middle:").grid(row=0, column=2)
        ttk.Label(pos_frame, textvariable=self.middle_pos_var).grid(row=0, column=3)
        ttk.Label(pos_frame, text="Right:").grid(row=0, column=4)
        ttk.Label(pos_frame, textvariable=self.right_pos_var).grid(row=0, column=5)

        # Canvas for visualizing the Enigma machine components and signal path
        self.canvas = tk.Canvas(self.root, width=800, height=600, background="white")
        self.canvas.grid(row=3, column=0, padx=10, pady=5)

    def setup_machine(self):
        try:
            rotors = self.rotor_names.get().split()
            rings = list(map(int, self.ring_settings.get().split()))
            positions = self.initial_positions.get().split()
            reflector = self.reflector_name.get()
            plug_pairs_input = self.plug_pairs.get()
            plug_pairs = sanitize_plugboard_input(plug_pairs_input) if plug_pairs_input else []

            self.enigma_machine = EnigmaMachine(rotors, rings, positions, reflector, plug_pairs)
            self.draw_enigma_machine()
            self.update_state_display()
            messagebox.showinfo("Success", "Machine configured successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup machine: {e}")

    def reset_machine(self):
        if self.enigma_machine:
            self.enigma_machine.reset()
            self.update_state_display()
        self.input_var.set("")
        self.encoded_var.set("")

    def on_key_press(self, event):
        ch = event.char.upper()
        if ch in ALPHABET:
            if not self.enigma_machine:
                messagebox.showerror("Error", "Machine not configured!")
                return
            out, path_dict = self.enigma_machine.encode_character(ch)
            self.input_var.set(self.input_var.get() + ch)
            self.encoded_var.set(self.encoded_var.get() + out)
            color = self.colors[self.color_index % len(self.colors)]
            self.color_index += 1
            self.canvas.delete("path")
            self.visualize_signal_path(path_dict, color=color)
            self.update_state_display()

    def update_state_display(self):
        if self.enigma_machine:
            self.left_pos_var.set(I2A[self.enigma_machine.left.pos])
            self.middle_pos_var.set(I2A[self.enigma_machine.middle.pos])
            self.right_pos_var.set(I2A[self.enigma_machine.right.pos])

    def draw_enigma_machine(self):
        """Draw a simplified diagram of the Enigma machine components on the canvas."""
        self.canvas.delete("all")

        # Draw labels
        self.canvas.create_text(40, self.base_y - 20, text="Keys/Lamps")
        self.canvas.create_text(100, self.base_y - 20, text="Plugboard")
        self.canvas.create_text(205, self.base_y - 20, text="Right Rotor")
        self.canvas.create_text(305, self.base_y - 20, text="Middle Rotor")
        self.canvas.create_text(405, self.base_y - 20, text="Left Rotor")
        self.canvas.create_text(500, self.base_y - 20, text="Reflector")

        # Draw fixed alphabets
        for pos_key in ['keyboard', 'plugboard', 'right_entry', 'right_exit', 'middle_entry', 'middle_exit', 'left_entry', 'left_exit', 'reflector']:
            self.draw_fixed_alphabet(self.component_positions[pos_key], pos_key)

        # Draw plugboard connections if machine is set
        if self.enigma_machine:
            pairs = self.enigma_machine._plug_pairs_list()
            for a, b in pairs:
                ia, ib = A2I[a], A2I[b]
                if ia > ib:
                    ia, ib = ib, ia
                    a, b = b, a
                y1 = self.base_y + ia * self.spacing
                y2 = self.base_y + ib * self.spacing
                # Draw arc to the left
                self.canvas.create_arc(60, y1, 140, y2, start=180, extent=180, style="arc", outline="gray")

            # Draw reflector connections
            seen = set()
            for i in range(26):
                j = self.enigma_machine.reflector_wiring[i]
                if i not in seen and j not in seen:
                    seen.add(i)
                    seen.add(j)
                    y1 = self.base_y + min(i, j) * self.spacing
                    y2 = self.base_y + max(i, j) * self.spacing
                    # Draw arc to the right
                    self.canvas.create_arc(460, y1, 540, y2, start=0, extent=180, style="arc", outline="gray")

    def draw_fixed_alphabet(self, x, pos_key):
        for i in range(26):
            y = self.base_y + i * self.spacing
            self.canvas.create_text(x, y, text=I2A[i], tags=("alphabet", f"alph_{pos_key}"))

    def visualize_signal_path(self, path_dict, color='red'):
        points = []
        def add_point(pos_key, letter):
            y = self.base_y + A2I[letter] * self.spacing
            points.append((self.component_positions[pos_key], y))

        add_point('keyboard', path_dict['input'])
        add_point('plugboard', path_dict['input'])
        add_point('plugboard', path_dict['plug_in_out'])
        add_point('right_entry', path_dict['plug_in_out'])
        add_point('right_exit', path_dict['right_out'])
        add_point('middle_entry', path_dict['right_out'])
        add_point('middle_exit', path_dict['middle_out'])
        add_point('left_entry', path_dict['middle_out'])
        add_point('left_exit', path_dict['left_out'])
        add_point('reflector', path_dict['left_out'])
        add_point('reflector', path_dict['refl_out'])
        add_point('left_exit', path_dict['refl_out'])
        add_point('left_entry', path_dict['left_back_out'])
        add_point('middle_exit', path_dict['left_back_out'])
        add_point('middle_entry', path_dict['middle_back_out'])
        add_point('right_exit', path_dict['middle_back_out'])
        add_point('right_entry', path_dict['right_back_out'])
        add_point('plugboard', path_dict['right_back_out'])
        add_point('plugboard', path_dict['plug_out_out'])
        add_point('keyboard', path_dict['plug_out_out'])

        # Schedule drawing of each segment with delay
        delay_ms = 1000  # 1 second per segment
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if (x1, y1) != (x2, y2):  # Skip zero-length lines
                self.root.after(i * delay_ms, lambda x1=x1, y1=y1, x2=x2, y2=y2, col=color: self.canvas.create_line(x1, y1, x2, y2, fill=col, width=3, tags="path"))

def main():
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
