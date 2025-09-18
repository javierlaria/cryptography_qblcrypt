import asyncio
import logging
import os
import json
import sys
from urllib.parse import urlparse
from nio import AsyncClient, MatrixRoom, RoomMessageText, LoginResponse, JoinResponse, RoomCreateResponse
from nio.exceptions import OlmUnverifiedDeviceError

# Configure logging for the application
# This sets the logging level to INFO, which will log informational messages and above
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables used throughout the program
# client: The Matrix client object for interacting with the Matrix server
# config_file: The file where configuration is stored (homeserver, user_id, etc.)
# user_keys: A dictionary mapping user IDs to their shared encryption keys (in memory only)
# current_room_id: The ID of the current Matrix room being used
client = None
config_file = "matrix_config.json"
user_keys = {}
current_room_id = None

# Function to validate URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and result.netloc
    except:
        return False

# This is the Vigenère cipher implementation. Students should replace these functions
# with their own custom cipher implementation for encryption and decryption.
# The custom cipher should take plaintext and key for encrypt, and ciphertext and key for decrypt.
# Ensure the custom cipher handles non-alphabetic characters appropriately if needed.
def prepare_text(text):
    text = text.upper().replace('J', 'I').replace(' ', '')
    i = 0
    digraphs = []
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            digraphs.append(a + 'X')
            i += 1
        else:
            digraphs.append(a + b)
            i += 2
    return digraphs

def generate_matrix(key):
    key = key.upper().replace('J', 'I')
    seen = set()
    matrix = []
    for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def caesar_shift(char, key_char):
    shift = ord(key_char.upper()) % 26
    base = ord('A')
    return chr((ord(char) - base + shift) % 26 + base)
    
def playfair_encrypt_pair(a, b, matrix):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def javier_encrypt(plaintext, key):
    digraphs = prepare_text(plaintext)
    matrix = generate_matrix(key)
    encrypted_text = ""

    for i, pair in enumerate(digraphs):
        playfair_result = playfair_encrypt_pair(pair[0], pair[1], matrix)
        
        kchar = key[i % len(key)].upper()
        xor_char1 = caesar_shift(playfair_result[0], kchar)
        xor_char2 = caesar_shift(playfair_result[1], kchar)
        
        encrypted_text += xor_char1 + xor_char2    
    return ''.join(encrypted_text)

def javier_decrypt(ciphertext, key):
    def generate_matrix(key):
        key = key.upper().replace('J', 'I')
        seen = set()
        matrix = []
        for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in seen and char.isalpha():
                seen.add(char)
                matrix.append(char)
        return [matrix[i*5:(i+1)*5] for i in range(5)]

    def find_position(matrix, char):
        for i, row in enumerate(matrix):
            for j, c in enumerate(row):
                if c == char:
                    return i, j
        return None
    def caesar_unshift(char, key_char):
        shift = ord(key_char.upper()) % 26
        base = ord('A')
        return chr((ord(char) - base - shift) % 26 + base)

    def playfair_decrypt_pair(a, b, matrix):
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            return matrix[row1][col2] + matrix[row2][col1]

    matrix = generate_matrix(key)
    decrypted_text= ""

    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]
        kchar = key[(i // 2) % len(key)].upper()

        plain_char1 = caesar_unshift(char1, kchar)
        plain_char2 = caesar_unshift(char2, kchar)

        plain_pair = playfair_decrypt_pair(plain_char1, plain_char2, matrix)
        decrypted_text += plain_pair
    
    return ''.join(decrypted_text)

# Functions for managing configuration
# These handle loading and saving the Matrix client configuration to a JSON file
def load_config():
    """Load Matrix client configuration from file if it exists, otherwise return defaults"""
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            pass  # If loading fails, fall back to defaults
    
    # Default configuration values
    return {
        "homeserver": "https://matrix.org",
        "user_id": "@atlantic_pacific:matrix.org",
        "device_id": "",
        "access_token": "",
        "room_id": ""
    }

def save_config(config):
    """Save Matrix client configuration to file"""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

# Functions for setting up the Matrix client and room
async def setup_client():
    """Set up the Matrix client with user-provided details or existing credentials"""
    global client, current_room_id
    
    config = load_config()
    
    print("Matrix Client Setup")
    print("===================")
    
    homeserver = config.get('homeserver', 'https://matrix.org')
    
    # Check if we have existing credentials
    if config.get('user_id') and config.get('access_token'):
        use_existing = input("Found existing credentials. Use them? (y/n): ").strip().lower()
        if use_existing == 'y':
            # Use existing homeserver from config
            homeserver = config['homeserver']
            # Validate the saved homeserver
            if not is_valid_url(homeserver):
                print("Saved homeserver URL is invalid. Please provide a valid one.")
                homeserver = input("Enter Matrix homeserver URL: ").strip()
                while not is_valid_url(homeserver):
                    print("Invalid homeserver URL. It must be a valid URL like https://matrix.org")
                    homeserver = input("Enter Matrix homeserver URL: ").strip()
                config['homeserver'] = homeserver
                save_config(config)
            
            user_id = config['user_id']
            # Create client with user_id
            client = AsyncClient(homeserver, user_id)
            client.device_id = config['device_id']
            client.access_token = config['access_token']
            client.user_id = user_id  # Ensure user_id is set
            
            if config.get('room_id'):
                current_room_id = config['room_id']
                print(f"Using existing room: {current_room_id}")
                return True
            else:
                print("No room configured. You'll need to join or create one.")
                return True  # Still return True, as login is done via token
    
    # Prompt for homeserver if new setup
    homeserver_input = input(f"Enter Matrix homeserver URL [{homeserver}]: ").strip()
    if homeserver_input:
        homeserver = homeserver_input
    while not is_valid_url(homeserver):
        print("Invalid homeserver URL. It must be a valid URL like https://matrix.org")
        homeserver = input("Enter Matrix homeserver URL: ").strip()
    
    # Get user_id for new login
    user_id = input("Matrix User ID (e.g., @username:matrix.org): ").strip()
    if not user_id:
        user_id = config.get('user_id', "@atlantic_pacific:matrix.org")
    
    # Create client with user_id
    client = AsyncClient(homeserver, user_id)
    
    password = input("Password: ").strip()
    
    # Try to login
    try:
        device_name = "VigenereDemoDevice"
        resp = await client.login(password=password, device_name=device_name)
        
        if isinstance(resp, LoginResponse):
            print("Login successful!")
            
            # Save credentials
            config['homeserver'] = homeserver
            config['user_id'] = resp.user_id or user_id
            config['device_id'] = resp.device_id
            config['access_token'] = resp.access_token
            save_config(config)
            
            client.user_id = config['user_id']  # Ensure user_id is set
            
            # Set up room
            await setup_room(config)
            return True
        else:
            print(f"Login failed: {resp}")
            print(f"Error message: {getattr(resp, 'message', 'No error message')}")
            return False
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def setup_room(config):
    """Set up the Matrix room by creating a new one or joining an existing one"""
    global current_room_id
    
    print("\nRoom Setup")
    print("==========")
    
    room_option = input("Join existing room (j) or create new room (c)? [j/c]: ").strip().lower()
    
    if room_option == 'c':
        # Create a new room
        room_name = input("Room name: ").strip()
        try:
            resp = await client.room_create(name=room_name)
            if isinstance(resp, RoomCreateResponse):
                current_room_id = resp.room_id
                config['room_id'] = current_room_id
                save_config(config)
                print(f"Created room: {current_room_id}")
            else:
                print(f"Failed to create room: {resp}")
        except Exception as e:
            print(f"Error creating room: {e}")
    else:
        # Join an existing room
        room_id_or_alias = input("Room ID or alias (e.g., #room:matrix.org): ").strip()
        try:
            resp = await client.join(room_id_or_alias)
            if isinstance(resp, JoinResponse):
                current_room_id = resp.room_id
                config['room_id'] = current_room_id
                save_config(config)
                print(f"Joined room: {current_room_id}")
            else:
                print(f"Failed to join room: {resp}")
        except Exception as e:
            print(f"Error joining room: {e}")

# Functions for viewing and decrypting room messages
async def view_room_messages():
    """View recent messages in the current room, attempting to decrypt encrypted ones if key is available"""
    global current_room_id
    
    if not current_room_id:
        print("No room configured. Please set up a room first.")
        return
    
    try:
        # Get room state to check if it's end-to-end encrypted by Matrix
        room_state = await client.room_get_state(current_room_id)
        
        # Check if room is encrypted (Matrix e2e encryption)
        is_encrypted = False
        for event in room_state.events:
            if (event.get('type') == 'm.room.encryption' and 
                event.get('content', {}).get('algorithm')):
                is_encrypted = True
                break
        
        # If room is Matrix e2e encrypted, warn user and exit
        if is_encrypted:
            print("This room uses Matrix end-to-end encryption. Use 'Decrypt messages' option to handle custom encryption.")
            return
        
        # Fetch recent messages (last 20)
        messages_response = await client.room_messages(
            current_room_id, 
            limit=20  # Get last 20 messages
        )
        
        if not hasattr(messages_response, 'chunk'):
            print("Failed to retrieve messages from the room.")
            return
        
        chunk = messages_response.chunk
        if not chunk:
            print("No recent messages in the room.")
            return
        
        print(f"\nRecent messages in room {current_room_id}:")
        print("=" * 60)
        
        # Reverse to show oldest to newest
        for event in reversed(chunk):
            if (hasattr(event, 'content') and 
                hasattr(event.content, 'body') and 
                hasattr(event, 'sender')):
                
                if hasattr(event, 'type') and event.type == 'm.room.message':
                    timestamp = getattr(event, 'origin_server_ts', 0)
                    if timestamp:
                        from datetime import datetime
                        dt = datetime.fromtimestamp(timestamp / 1000)
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time_str = "Unknown time"
                    
                    body = event.content.body
                    if body.startswith("ENC:"):
                        ciphertext = body[4:]
                        key = user_keys.get(event.sender)
                        if key:
                            try:
                                # Note: Replace vigenere_decrypt with your custom decrypt function
                                decrypted = javier_decrypt(ciphertext, key)
                                print(f"[{time_str}] {event.sender}: {decrypted} (decrypted)")
                            except Exception as e:
                                print(f"[{time_str}] {event.sender}: {body} (decryption failed: {e})")
                        else:
                            print(f"[{time_str}] {event.sender}: {body} (encrypted, no key available)")
                    else:
                        print(f"[{time_str}] {event.sender}: {body}")
        
        print("=" * 60)
            
    except Exception as e:
        print(f"Error viewing room messages: {e}")
        import traceback
        traceback.print_exc()

async def decrypt_room_messages():
    """Decrypt and view recent messages from the room, prompting for keys for each encrypted message"""
    global current_room_id
    
    if not current_room_id:
        print("No room configured. Please set up a room first.")
        return
    
    try:
        # Get room state to check if it's end-to-end encrypted by Matrix
        room_state = await client.room_get_state(current_room_id)
        
        # Check if room is encrypted (Matrix e2e encryption)
        is_encrypted = False
        for event in room_state.events:
            if (event.get('type') == 'm.room.encryption' and 
                event.get('content', {}).get('algorithm')):
                is_encrypted = True
                break
        
        # Note: This room uses Matrix end-to-end encryption. Attempting to decrypt custom 'ENC:' messages.
        if is_encrypted:
            print("Note: This room uses Matrix end-to-end encryption. Attempting to decrypt custom 'ENC:' messages.")
        
        # Fetch recent messages (last 20)
        messages_response = await client.room_messages(
            current_room_id, 
            limit=20  # Get last 20 messages
        )
        
        if not hasattr(messages_response, 'chunk'):
            print("Failed to retrieve messages from the room.")
            return
        
        chunk = messages_response.chunk
        if not chunk:
            print("No recent messages in the room.")
            return
        
        print(f"\nRecent messages in room {current_room_id} (with decryption):")
        print("=" * 60)
        
        # Keep track of processed senders to avoid repeated key prompts
        processed_senders = set()
        
        # Reverse to show oldest to newest
        for event in reversed(chunk):
            if (hasattr(event, 'content') and 
                hasattr(event.content, 'body') and 
                hasattr(event, 'sender')):
                
                if hasattr(event, 'type') and event.type == 'm.room.message':
                    timestamp = getattr(event, 'origin_server_ts', 0)
                    if timestamp:
                        from datetime import datetime
                        dt = datetime.fromtimestamp(timestamp / 1000)
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time_str = "Unknown time"
                    
                    body = event.content.body
                    if body.startswith("ENC:"):
                        ciphertext = body[4:]
                        sender = event.sender
                        
                        # Only prompt for key if not available and not processed this session
                        if sender not in user_keys and sender not in processed_senders:
                            print(f"Encrypted message from {sender}: {body}")
                            key = input(f"Enter encryption key for {sender} (or press Enter to skip): ").strip()
                            if key:
                                user_keys[sender] = key
                            processed_senders.add(sender)
                        
                        key = user_keys.get(sender)
                        if key:
                            try:
                                # Note: Replace vigenere_decrypt with your custom decrypt function
                                decrypted = javier_decrypt(ciphertext, key)
                                print(f"[{time_str}] {sender}: {decrypted} (decrypted)")
                            except Exception as e:
                                print(f"[{time_str}] {sender}: {body} (decryption failed: {e})")
                        else:
                            print(f"[{time_str}] {sender}: {body} (encrypted, no key available)")
                    else:
                        print(f"[{time_str}] {event.sender}: {body}")
        
        print("=" * 60)
            
    except Exception as e:
        print(f"Error decrypting room messages: {e}")
        import traceback
        traceback.print_exc()

# Matrix event handlers
async def message_callback(room: MatrixRoom, event: RoomMessageText):
    """Handle incoming messages in real-time, attempting to decrypt if encrypted"""
    try:
        # Check if the message starts with our custom encryption prefix
        if event.body.startswith("ENC:"):
            ciphertext = event.body[4:]
            user_id = event.sender
            
            if user_id in user_keys:
                key = user_keys[user_id]
                # Note: Replace vigenere_decrypt with your custom decrypt function
                decrypted = javier_decrypt(ciphertext, key)
                print(f"\n🔓 Decrypted message from {user_id}: {decrypted}")
            else:
                print(f"\n⚠️  Received encrypted message from {user_id}, but no key available")
                print(f"Message: {ciphertext}")
        else:
            print(f"\n📨 Message from {event.sender}: {event.body}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

async def start_sync():
    """Start syncing with the Matrix server to receive real-time events"""
    if client:
        # Add the message callback for text messages
        client.add_event_callback(message_callback, RoomMessageText)
        try:
            while True:
                # Sync with timeout of 30 seconds
                await client.sync(timeout=30000, full_state=False)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Sync error: {e}")

# Function for sending messages
async def send_encrypted_message(message, key):
    """Encrypt and send a message to the current Matrix room"""
    global current_room_id
    
    if not current_room_id:
        print("No room configured. Please set up a room first.")
        return False
    
    # Note: Replace vigenere_encrypt with your custom encrypt function
    encrypted = javier_encrypt(message, key)
    try:
        resp = await client.room_send(
            room_id=current_room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": f"ENC:{encrypted}"
            }
        )
        # Check for successful send (has event_id)
        if hasattr(resp, 'event_id') and resp.event_id:
            print("✅ Encrypted message sent successfully")
            return True
        else:
            print(f"Send failed: {resp}")
            return False
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False

# Main application loop
async def main_loop():
    """Main application loop handling user input and menu options"""
    global current_room_id
    
    # Set up the client initially
    if not await setup_client():
        print("Failed to set up client. Exiting.")
        return
    
    # Load room ID from config if not already set
    config = load_config()
    if not current_room_id and config.get('room_id'):
        current_room_id = config['room_id']
    
    # Start real-time syncing in the background
    asyncio.create_task(start_sync())
    
    # Perform an initial sync to ensure state is up to date
    await client.sync(full_state=True)
    
    while True:
        print("\n" + "="*50)
        print("Vigenère Encrypted Matrix Messenger")
        print("="*50)
        print(f"User: {client.user_id if client and client.user_id else 'Not set'}")
        print(f"Room: {current_room_id or 'Not set'}")
        print("="*50)
        print("Options:")
        print("1. Set encryption key for a user")
        print("2. Send encrypted message")
        print("3. Change room")
        print("4. Reconfigure client")
        print("5. View room messages")
        print("6. Decrypt messages from room")
        print("7. Exit")
        
        try:
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                # Set a key for a specific user
                user_id = input("Enter user ID (e.g., @user:matrix.org): ").strip()
                key = input("Enter encryption key: ").strip()
                if user_id and key:
                    user_keys[user_id] = key
                    print(f"Key set for {user_id}")
                else:
                    print("User ID and key cannot be empty.")
                    
            elif choice == "2":
                # Send an encrypted message using a set key
                if not user_keys:
                    print("No encryption keys set. Please set a key first.")
                    continue
                    
                if not current_room_id:
                    print("No room configured. Please set up a room first.")
                    continue

                # List available users with keys
                print("Available users:")
                for i, uid in enumerate(user_keys.keys(), 1):
                    print(f"{i}. {uid}")
                try:
                    sel = int(input("Select user to send to (number): ")) - 1
                    users_list = list(user_keys.items())
                    if 0 <= sel < len(users_list):
                        selected_user_id, key = users_list[sel]
                        message = input("Enter message to encrypt and send: ").strip()
                        if message:
                            await send_encrypted_message(message, key)
                            print(f"Encrypted and sent using key for {selected_user_id}.")
                        else:
                            print("Message cannot be empty.")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                
            elif choice == "3":
                # Change the current room
                await setup_room(load_config())
                
            elif choice == "4":
                # Reconfigure the client
                if await setup_client():
                    config = load_config()
                    if config.get('room_id'):
                        current_room_id = config['room_id']
                    # Restart sync task
                    asyncio.create_task(start_sync())
            
            elif choice == "5":
                # View messages (decrypt if key available)
                await view_room_messages()
            
            elif choice == "6":
                # Decrypt messages, prompting for keys if needed
                await decrypt_room_messages()
                
            elif choice == "7":
                print("Exiting...")
                if client:
                    await client.close()
                break
                
            else:
                print("Invalid option. Please choose 1-7.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            if client:
                await client.close()
            break
        except Exception as e:
            print(f"Error: {e}")

# Entry point of the program
if __name__ == "__main__":
    try:
        # Run the main async loop
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Ensure client is closed on exit
        if client:
            asyncio.run(client.close())