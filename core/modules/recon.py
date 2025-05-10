from core.recon import run_auto_recon

StealthButton(self.content_frame, text="Start Recon", command=self.start_recon).pack()

def start_recon(self):
    self.status_bar.update_status("Recon running...")
    self.popup("Launching recon...")
    run_auto_recon(target="127.0.0.1")  # real logic hook
