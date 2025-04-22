from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}██╗  ██╗██╗   ██╗██╗  ██╗███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
{Fore.RED}██║ ██╔╝██║   ██║██║ ██╔╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
{Fore.RED}█████╔╝ ██║   ██║█████╔╝ █████╗  ███████║   ██║   ██║   ██║██████╔╝
{Fore.RED}██╔═██╗ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██║   ██║   ██║   ██║██╔═══╝ 
{Fore.RED}██║  ██╗╚██████╔╝██║  ██╗███████╗██║  ██║   ██║   ╚██████╔╝██║     
{Fore.RED}╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     
        {Fore.YELLOW}X-VECTOR PRO{Fore.WHITE} | {Fore.CYAN}Silent. Adaptive. Lethal.{Style.RESET_ALL}
    """
    print(banner)
