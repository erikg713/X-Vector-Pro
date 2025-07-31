import ssl, socket

def get_ssl_expiry(domain: str) -> str:
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            return cert.get('notAfter', 'unknown')
