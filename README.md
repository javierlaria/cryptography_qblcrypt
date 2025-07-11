````markdown
# Applied Cryptography & Secure Systems

![Cryptography Banner](https://placehold.co/1200x300/4338ca/ffffff?text=Applied+Cryptography+%26+Secure+Systems)

Welcome to the official GitHub repository for the Applied Cryptography course. This repository contains all the practical lab exercises you will need for the semester. Our philosophy is simple: **you learn by doing**. Forget endless static slides; here, you will write code, break ciphers, analyze real network traffic, and build a portfolio of practical skills.

This course is designed to be highly interactive. We will use a combination of Python programming, industry-standard security tools, and modern development practices to explore the fascinating world of cryptography.

---

## 🚀 Getting Started: Your Environment Setup

Before you can begin the first lab, you need to set up your environment. All work will be done inside a **Kali Linux Virtual Machine (VM)** to ensure everyone has the same tools and capabilities.

### 1. Install Your Virtual Lab
- **Download Kali Linux:** Get the latest version of the Kali Linux VM image (we recommend the VMware or VirtualBox version) from the [official website](https://www.kali.org/get-kali/#kali-virtual-machines).
- **Import the VM:** Follow the instructions for your virtualization software (VMware Player/Workstation or VirtualBox) to import and run the Kali VM.

### 2. Configure Your Tools
Open a terminal in your new Kali VM and run the following commands to install the essential software for this course:

```bash
# Update package lists
sudo apt update

# Install Jupyter Lab, Git, and Python's package manager
sudo apt install -y jupyter-lab git python3-pip

# Install required Python libraries
pip install cryptography pycryptodome argon2-cffi bcrypt pytest
````

### 3\. Set Up Your GitHub Account

  - **Create an Account:** If you don't already have one, create a free account on [GitHub.com](https://github.com/).
  - **Configure Git:** Introduce yourself to Git. This name will be attached to all of your commits.
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

-----

## 🛠️ How to Use This Repository: The Git Workflow

You will **not** write code directly in this repository. Instead, you will create your own copy, work on it, and save your progress using version control. Follow this process for **every lab**.

1.  **Fork this Repository:** Click the **"Fork"** button in the top-right corner of this page. This creates your own personal copy of the entire repository under your GitHub account.

2.  **Clone Your Fork:** In your Kali VM's terminal, clone **your forked repository**, not the original one. Replace `<YourUsername>` with your GitHub username.

    ```bash
    git clone [https://github.com/](https://github.com/)<YourUsername>/Cryptography-Course-Madrid.git
    cd Cryptography-Course-Madrid
    ```

3.  **Create a Branch:** Before starting a lab, create a new branch for your work. This keeps your main branch clean and organizes your solutions.

    ```bash
    # Example for the first lab
    git checkout -b lab01-solution
    ```

4.  **Work on the Lab:** Navigate to the lab's directory (e.g., `cd 01_Classical_Ciphers/`) and complete the tasks as described in its `README.md` file.

5.  **Commit Your Changes:** Once you have completed the exercise, commit your work with a clear message describing what you've done.

    ```bash
    # Add the specific file(s) you changed
    git add vigenere_breaker.py

    # Commit with a message
    git commit -m "Complete Vigenère breaker implementation"
    ```

6.  **Push Your Branch to GitHub:** Save your work to your forked repository on GitHub.

    ```bash
    # The -u flag sets the upstream branch for future pushes
    git push -u origin lab01-solution
    ```

This workflow is standard practice in software development and is a key skill you will take away from this course.

-----

## 📚 Course Structure & Labs

This course is divided into six major sections, each with a corresponding practical lab.

| Lab \# | Topic                                  | Directory                                        | Key Skills Taught                               |
| :---- | :------------------------------------- | :----------------------------------------------- | :---------------------------------------------- |
| 01    | Classical Cryptanalysis                | [`01_Classical_Ciphers/`](https://www.google.com/search?q=./01_Classical_Ciphers/) | Python, Frequency Analysis, Problem Solving     |
| 02    | Modern Symmetric Encryption            | [`02_Symmetric_Encryption/`](https://www.google.com/search?q=./02_Symmetric_Encryption/) | AES-GCM, `cryptography` library, Tool Building    |
| 03    | Password Hashing & Security          | [`03_Hashing_Passwords/`](https://www.google.com/search?q=./03_Hashing_Passwords/) | `bcrypt`/`argon2`, Secure Password Storage        |
| 04    | Asymmetric Cryptography & Signatures   | [`04_Asymmetric_Crypto/`](https://www.google.com/search?q=./04_Asymmetric_Crypto/) | RSA, Digital Signatures, `openssl` concepts     |
| 05    | Public Key Infrastructure (PKI)        | [`05_PKI_Validation/`](https://www.google.com/search?q=./05_PKI_Validation/)     | `openssl` CLI, Certificate Chain Validation     |
| 06    | Network Traffic Analysis               | [`06_Network_Forensics/`](https://www.google.com/search?q=./06_Network_Forensics/) | Wireshark, TLS Protocol Analysis, Forensics     |

-----

## 💡 A Note on Ethics

The tools and techniques taught in this course (especially those involving Kali Linux and hardware like the Flipper Zero) are powerful. They are taught for one reason: **to understand how to build secure systems by learning to think like an attacker**. Using this knowledge for any unauthorized activity is unethical, illegal, and a violation of the course policy. We will only ever conduct analysis on systems and hardware we own or have explicit permission to test.

## 🤖 Using LLMs for Deeper Learning

You are encouraged to use Large Language Models (LLMs) like ChatGPT or Google Gemini to go one step further in your learning. Use them to ask "what if" questions or to get clearer explanations of complex topics.

**Example "Deep Dive" Prompt:**

> "Act as a cybersecurity protocol designer. Explain the concept of **Forward Secrecy** as it applies to TLS. Why does a handshake using an ephemeral Diffie-Hellman key exchange (DHE/ECDHE) provide this property, while a classic RSA key exchange does not? Describe a scenario where the lack of forward secrecy would be catastrophic."

```
```