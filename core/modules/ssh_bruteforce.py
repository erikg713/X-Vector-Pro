import paramiko
from rich import print

def try_ssh(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        print(f"[green]Success! Logged into {ip}[/]")
        return True
    except:
        print(f"[red]Failed login to {ip} with {username}/{password}[/]")
        return False
    finally:
        client.close()

if __name__ == "__main__":
    ip = input("Target IP: ")
    user = input("Username: ")
    passwd = input("Password: ")
    try_ssh(ip, user, passwd)
