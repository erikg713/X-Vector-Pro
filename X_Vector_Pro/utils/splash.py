import tkinter as tk
from tkinter import ttk
import time
import threading

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("400x200")
        self.root.configure(bg="#2E2E2E")

        # Add label for splash text
        self.label = tk.Label(self.root, text="Welcome to X-Vector Pro!", font=("Arial", 18, "bold"), fg="white", bg="#2E2E2E")
        self.label.pack(pady=30)

        # Create a label for the loading spinner (animation)
        self.spinner_label = tk.Label(self.root, text=".", font=("Arial", 30, "bold"), fg="white", bg="#2E2E2E")
        self.spinner_label.pack(pady=20)
        
        # Start the animation
        self._animate_spinner()

        # Add a close button for the splash screen
        self.close_button = tk.Button(self.root, text="Close", state=tk.DISABLED, command=self.close_splash)
        self.close_button.pack(pady=10)

    def _animate_spinner(self):
        """Animate the loading spinner with dots."""
        # This function will add dots incrementally to create the animation effect
        self.spinner_text = ['.', '..', '...']
        self.dot_index = 0
        self._update_spinner()

    def _update_spinner(self):
        """Update the spinner text."""
        self.spinner_label.config(text=self.spinner_text[self.dot_index])
        self.dot_index = (self.dot_index + 1) % len(self.spinner_text)

        # Keep updating every 500 ms to simulate loading
        self.root.after(500, self._update_spinner)

    def close_splash(self):
        """Method to close the splash screen."""
        self.root.destroy()

    def finish_loading(self):
        """Simulate some background task and close splash screen."""
        # Simulate loading process (this can be replaced with actual loading logic)
        time.sleep(5)  # Simulate loading time
        
        # When loading is complete, stop the spinner and close splash screen
        self.close_button.config(state=tk.NORMAL)
        self.label.config(text="Loading Complete!", fg="green")
        time.sleep(1)
        self.close_splash()

def start_splash():
    """Start the splash screen in a separate thread."""
    root = tk.Tk()
    splash = SplashScreen(root)
    
    # Run the loading process in a separate thread to avoid blocking the GUI
    threading.Thread(target=splash.finish_loading).start()
    
    root.mainloop()

if __name__ == "__main__":
    start_splash()
