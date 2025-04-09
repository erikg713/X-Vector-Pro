# GUI-Wordpress-Bruteforce-Tool
---
This GUI app will let you:

Input the target URL

Enter one or more usernames

Load a password list file

Start brute-forcing with a Start button

See hits or errors in a log window

Save valid credentials to a file (hits.txt)

---
# SETUP TO RUN ON KALI

# Install Tkinter if needed #

# Tkinter should come pre-installed, but just in case:

sudo apt update
sudo apt install python3-tk

# Save the Script

# In terminal: #

nano wp_gui_brute.py

# Paste the full script above. Then:

# Press Ctrl + O → Enter

# Press Ctrl + X to exit

---

# Run the GUI Tool

python3 wp_gui_brute.py

# You’ll see a nice GUI pop up with:

# Target field (default: zayachek)

# Multi-line usernames box

# File selector for password list

Results window and a Start button



---

4. After It Runs

Valid hits are saved in hits.txt

You can re-use these logins in browser, Burp, or automation
