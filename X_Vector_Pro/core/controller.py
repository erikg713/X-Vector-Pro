from core.brute import xmlrpc_brute
from utils.logger import log

def start_brute_force(url, username):
    log("[*] Launching XML-RPC brute force...")
    xmlrpc_brute(url, username)
