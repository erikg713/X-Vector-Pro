import socket
import requests

def get_local_ip():
    """Get the local machine's IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Doesn't even have to be connected to the internet
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def check_internet_connection(url='http://google.com', timeout=5):
    """Check if the machine can reach the internet."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_public_ip():
    """Get the public IP address by querying an external service."""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException:
        return None
