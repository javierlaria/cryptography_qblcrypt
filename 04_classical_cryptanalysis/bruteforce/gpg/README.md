🔐 Step 1: Symmetric Encryption with GPG
Create a plaintext file:

bash
echo "This is a secret file for password cracking." > message.txt
Encrypt it with a simple password (e.g., 1234):

bash
gpg --cipher-algo CAST5 --allow-old-cipher-algos -c message.txt
Respond to the prompt by entering your password.

✅ This creates message.txt.gpg.

🧱 Step 2: Extract the Hash with gpg2john
Convert the GPG file into a hash format that John can crack:

bash
gpg2john message.txt.gpg > gpg_hash.txt
Check the file:

bash
cat gpg_hash.txt
You should see something like this:

text
message.txt.gpg:$gpg$0*17*...
🪓 Step 3: Crack with John the Ripper
📖 Option 1: Use a Wordlist
Try cracking using the RockYou wordlist (commonly pre-installed on Kali):

bash
john gpg_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
Or use your own custom wordlist:

bash
john gpg_hash.txt --wordlist=mylist.txt
🧠 Option 2: Brute-Force Attack
Try all combinations up to 5 characters:

bash
john gpg_hash.txt --incremental=ASCII --min-length=1 --max-length=5
✅ Step 4: Show the Cracked Password
After cracking, reveal the recovered password with:

bash
john --show gpg_hash.txt
Example output:

text
message.txt.gpg:1234
Success! You've recovered the password used to encrypt the GPG file.
