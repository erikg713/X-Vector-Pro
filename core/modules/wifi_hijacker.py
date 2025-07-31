import subprocess

def list_networks():
    output = subprocess.check_output(["netsh", "wlan", "show", "networks"]).decode()
    print(output)

if __name__ == "__main__":
    list_networks()
