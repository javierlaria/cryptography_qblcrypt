import requests
import time

class CryptographicAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

    def send_to_lechat(self, message, max_retries=3):
        """Send message to Mistral Le Chat API with retry logic."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-large-latest",
            "messages": [{"role": "user", "content": message}]
        }
        for attempt in range(max_retries):
            try:
                response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                else:
                    return f"Failed to communicate with Mistral API. Status code: {response.status_code}"
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return f"An error occurred while trying to connect to Mistral API: {e}"
        return "Max retries reached. Could not connect to Mistral API."

    def try_all_ciphers(self, text):
        """Try to decode the text using all supported ciphers."""
        results = {}

        # Vigenère with common keys
        common_keys = ["SECRET", "KEY", "PASSWORD", "MISTRAL", "LECHAT"]
        for key in common_keys:
            results[f'Vigenère (key={key})'] = self.vigenere_cipher(text, key, decode=True)

        # Transposition with common column counts
        for cols in [5, 6, 7, 8, 9, 10]:
            results[f'Transposition (cols={cols})'] = self.transposition_cipher(text, cols, decode=True)

        # Mono-alphabetic (Caesar) with common shifts
        for shift in range(1, 26):
            results[f'Caesar (shift={shift})'] = self.mono_alphabetic_cipher(text, shift, decode=True)

        # Enigma with common settings
        for shift in [1, 3, 5, 7]:
            results[f'Enigma (shift={shift})'] = self.enigma_machine(text, [shift], decode=True)

        return results

    @staticmethod
    def vigenere_cipher(text, key, decode=False):
        """Decode text using Vigenère cipher."""
        result = []
        key_index = 0
        key = key.upper()
        for char in text.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                if decode:
                    shift = -shift
                new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                result.append(new_char)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def transposition_cipher(text, key, decode=False):
        """Decode text using Transposition cipher."""
        if not key:
            return text
        text = text.replace(" ", "")
        num_columns = key
        num_rows = (len(text) + num_columns - 1) // num_columns
        grid = [list(text[i*num_columns : (i+1)*num_columns].ljust(num_columns)) for i in range(num_rows)]
        if decode:
            transposed = list(zip(*grid))
            result = "".join(["".join(row) for row in transposed])
        else:
            result = "".join(["".join([row[i] for row in grid if i < len(row)]) for i in range(num_columns)])
        return result

    @staticmethod
    def mono_alphabetic_cipher(text, shift, decode=False):
        """Decode text using mono-alphabetic cipher (Caesar shift)."""
        result = []
        shift = -shift if decode else shift
        for char in text.upper():
            if char.isalpha():
                new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                result.append(new_char)
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def enigma_machine(text, settings, decode=False):
        """Simulate a very basic Enigma-like machine decoding."""
        result = []
        shift = settings[0] if isinstance(settings, list) else 1
        for char in text.upper():
            if char.isalpha():
                new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                result.append(new_char)
            else:
                result.append(char)
        return ''.join(result)

def main():
    api_key = input("Enter your Mistral API key: ")
    agent = CryptographicAgent(api_key)

    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        # Try all ciphers
        decoded_attempts = agent.try_all_ciphers(user_input)
        summary = "Decoding attempts:\n" + "\n".join([f"{k}: {v[:50]}..." for k, v in decoded_attempts.items()])

        # Send summary to Mistral for analysis
        response = agent.send_to_lechat(f"Original: {user_input}\n{summary}\nWhat is the most likely plaintext?")
        print("Mistral Analysis:", response)

if __name__ == "__main__":
    main()

