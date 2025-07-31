import psutil
from rich import print

def system_inspect():
    print("[bold cyan]CPU Usage:[/]", psutil.cpu_percent(interval=1))
    print("[bold green]Memory Info:[/]", psutil.virtual_memory())
    print("[bold yellow]Disk Info:[/]", psutil.disk_partitions())

if __name__ == "__main__":
    system_inspect()
