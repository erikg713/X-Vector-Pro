import customtkinter as ctk
import threading
import time

class ToastManager:
    def __init__(self, root):
        self.root = root

    def show(self, message, level="info", duration=3000):
        colors = {
            "info": "#1f6aa5",
            "success": "#2e8b57",
            "error": "#a52a2a"
        }
        toast = ctk.CTkLabel(
            self.root,
            text=message,
            text_color="white",
            fg_color=colors.get(level, "#1f6aa5"),
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            padx=15,
            pady=8
        )
        toast.place(relx=0.5, rely=0.95, anchor="s")
        toast.attributes = {"alpha": 0}
        toast.after(10, lambda: self._fade_in(toast, 0))

        def auto_dismiss():
            time.sleep(duration / 1000)
            self._fade_out(toast, 1.0)

        threading.Thread(target=auto_dismiss, daemon=True).start()

    def _fade_in(self, widget, alpha):
        if alpha >= 1.0:
            return
        widget.attributes["alpha"] = alpha
        widget.configure(fg_color=widget._fg_color)
        widget.update()
        widget.after(30, lambda: self._fade_in(widget, alpha + 0.1))

    def _fade_out(self, widget, alpha):
        if alpha <= 0:
            widget.destroy()
            return
        widget.attributes["alpha"] = alpha
        widget.configure(fg_color=widget._fg_color)
        widget.update()
        widget.after(30, lambda: self._fade_out(widget, alpha - 0.1))
