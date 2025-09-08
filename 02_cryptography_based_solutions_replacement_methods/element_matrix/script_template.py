from nio import AsyncClient, LoginResponse
import asyncio

HOMESERVER = "https://matrix.org"
USERNAME = "@atlantic_pacific:matrix.org"
PASSWORD = "Uranium098@"
ROOM_ID = "eye_of_the_sahara:matrix.org"
KEY = "monarchy"  # Vigenere key

async def main():
    client = AsyncClient(HOMESERVER, USERNAME)
    login = await client.login(PASSWORD)

    # Send encrypted message
    plaintext = "MEET AT NOON"
    ciphertext = vigenere_encrypt(plaintext, KEY)
    await client.room_send(
        room_id=ROOM_ID,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": ciphertext}
    )

    # Wait and receive messages
    async def message_callback(room, event):
        if event["type"] == "m.room.message":
            body = event["content"].get("body")
            print("Received ciphertext:", body)
            print("Decrypted:", vigenere_decrypt(body, KEY))

    client.add_event_callback(message_callback, ("m.room.message",))
    await client.sync_forever(timeout=30000)

asyncio.run(main())
