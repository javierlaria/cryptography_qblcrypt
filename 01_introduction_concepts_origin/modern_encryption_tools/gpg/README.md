📁 Step 1: Create a Test File
Let's create a plaintext file to encrypt:

bash
echo "This is a secret message for the cryptography class." > message.txt
🔐 Step 2: Encrypt the File (Symmetric Encryption)
Use symmetric encryption (-c) to encrypt the file with a password (known only to you):

bash
gpg -c message.txt
This command will:

Prompt you for a passphrase (use something simple like test123 if you're doing a lab).

Create an encrypted file: message.txt.gpg

💡 By default, GPG will use AES-128 for encryption.

🔁 Change the Cipher Algorithm (Optional)
You can specify a cipher explicitly using --cipher-algo.

Example — AES256:

bash
gpg --cipher-algo AES256 -c message.txt
Example — older/weaker algorithm (CAST5):

bash
gpg --cipher-algo CAST5 --allow-old-cipher-algos -c message.txt
⚠️ Warning: CAST5 is outdated — use only for educational purposes.

🔍 Step 3: Check What Algorithm Was Used
After encryption, check the encryption details using:

bash
gpg --list-packets message.txt.gpg
You'll see output like:

text
:encrypted data packet:
    cipher algorithm: CAST5
This confirms the algorithm used (e.g., AES, AES256, CAST5, etc.).

🔓 Step 4: Decrypt the File
➕ Method 1: Automatic (Writes to Original File)
bash
gpg message.txt.gpg
GPG will try to decrypt and write to message.txt.
