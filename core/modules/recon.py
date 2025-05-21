from core.recon import run_auto_recon
import logging
from tkinter import Entry, Button, Frame

class ReconModule:
    def __init__(self, parent_frame: Frame):
        self.parent_frame = parent_frame
        self.target_input = Entry(self.parent_frame, width=30)
        self.target_input.pack(pady=5)
        self.target_input.insert(0, "Enter target IP/Domain")
        
        Button(self.parent_frame, text="Start Recon", command=self.start_recon).pack(pady=5)
        self.status_bar = None  # Placeholder for the status bar instance, set externally

        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def set_status_bar(self, status_bar):
        """Set the status bar instance for this module."""
        self.status_bar = status_bar

    def start_recon(self):
        """Start the reconnaissance process."""
        target = self.target_input.get().strip()
        if not target:
            self.popup("Please enter a valid target!")
            return
        
        try:
            if self.status_bar:
                self.status_bar.update_status("Recon running...")

            self.popup(f"Launching recon on target: {target}")
            logging.info(f"Starting reconnaissance on target: {target}")
            
            # Call the actual recon function
            run_auto_recon(target=target)
            
            if self.status_bar:
                self.status_bar.update_status("Recon completed!")
            logging.info("Reconnaissance completed successfully.")
        
        except Exception as e:
            error_message = f"Recon failed: {e}"
            logging.error(error_message)
            self.popup(error_message)
    
    def popup(self, message: str):
        """Display a popup message."""
        # Replace with actual implementation for showing a popup
        logging.info(f"Popup message: {message}")
