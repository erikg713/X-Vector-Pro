from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the ASCII banner as a constant
BANNER = f"""
{Fore.YELLOW}▀▄▀ ▄▄ █░█ █▀▀ █▀▀ ▀█▀ █▀█ █▀█ ▄▄ █▀█ █▀█ █▀█
█░█ ░░ ▀▄▀ ██▄ █▄▄ ░█░ █▄█ █▀▄ ░░ █▀▀ █▀▄ █▄█{Style.RESET_ALL}
{Fore.CYAN}+---------------------------------------------------------+
| Recon - Information Gathering                           |
|---------------------------------------------------------|
| [Target Input]         [ Start Recon ] [ Stop Recon ]   |
|                                                           |
| [ ] Reconnaissance                                        |
| [ ] Port Scanning                                         |
| [ ] Vulnerability Scan                                    |
| [ ] Web Brute Force                                       |
| [ ] Subdomain Enumeration                                 |
|                                                           |
| [Progress Bar]                                            |
|                                                           |
| [----------------- Live Logs Text Box ------------------] |
+---------------------------------------------------------+
| Settings | Reports | About                                |
+---------------------------------------------------------+
{Fore.WHITE}X-VECTOR PRO | Silent. Adaptive. Lethal.{Style.RESET_ALL}
"""

def print_banner():
    """
    Prints the ASCII banner to the console.
    """
    print(BANNER)

if __name__ == "__main__":
    print_banner()
