# [CHALLENGE] Intercepted Transmission - Project "Whisperfall"

**Team,**

Last week we covered the fundamentals of classical ciphers. This week, we're putting that theory into practice. Our monitoring systems have intercepted a fragmented transmission from a rival group. We believe it's encrypted with a custom, non-standard classical cipher they've codenamed "Whisperfall." Their methods are sloppy, but we need to prove it.

Your mission is to break their cipher, recover the original message, analyze the protocol's weaknesses, and then design a superior version.

---

### **Phase 1: Reconnaissance & Decryption**

Here is the intercepted ciphertext. We believe the original message was a quote about secrecy or privacy.

>Ciphertext: YOXKR_GPRKF_YC_KVBFO_AYBAG_KYYAC_VBGAI_FKDBA_YBRKR_KYYAC_VBGAR


We also recovered a partial configuration note from their operative:

> "Protocol: Whisperfall. Key 1: `LEGION`. Key 2: `3`. Standard alphabet. They'll never figure out our combo."

**Your Objective:**
Decrypt the message. This cipher is a **hybrid**; it uses more than one classical technique. You'll need to figure out the sequence of operations.

---

### **Phase 2: Vulnerability Analysis**

Once you have the plaintext, your job isn't done. You need to write a brief report on the "Whisperfall" protocol's weaknesses.

**Your analysis should answer:**
1.  What are the primary families of ciphers used?
2.  How does Kerckhoffs's Principle apply here?
3.  Analyze the key space. Is it sufficient? Why or why not?

---

### **Phase 3: Counter-Operation (The Homework)**

Design and build your own simple, pen-and-paper-style encryption scheme in Python.

**Your Objective:**
Create a Python script named `yourname_cipher.py` that implements your own custom encryption and decryption functions. Bonus points for creating a simple but effective hybrid cipher. Your code must be well-commented.

---

### **Final Debriefing**

Reply to the forum thread with:
1.  The Decrypted Plaintext.
2.  Your Vulnerability Report.
3.  Your Python Script.
4.  (BONUS) A link to your GitHub pull request.
