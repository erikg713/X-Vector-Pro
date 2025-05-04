import os
import random
import sys

WORDLIST_DIR = os.path.join(os.path.dirname(__file__), '..', 'wordlists')


class WordlistCombiner:
    def __init__(self):
        self.output_dir = WORDLIST_DIR

    def detect_format(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        return ext if ext else '.txt'

    def load(self, filename):
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            print(f"[+] Loaded {len(lines)} lines from '{filename}'")
            return lines
        except FileNotFoundError:
            print(f"[!] File not found: {path}")
            return []

    def display_progress(self, current, total):
        percent = (current / total) * 100
        sys.stdout.write(f"\r[*] Progress: {percent:.2f}%")
        sys.stdout.flush()

    def combine(self, file1, file2, separator=":", shuffle=True, dedupe=True, output_name="combined_hybrid.txt", show_progress=True):
        list1 = self.load(file1)
        list2 = self.load(file2)

        total = len(list1) * len(list2)
        combined = []

        for i, a in enumerate(list1):
            for j, b in enumerate(list2):
                combined.append(f"{a}{separator}{b}")
                if show_progress and (i * len(list2) + j) % 1000 == 0:
                    self.display_progress(i * len(list2) + j, total)

        if show_progress:
            self.display_progress(total, total)
            print("\n[+] Combination complete.")

        if dedupe:
            before = len(combined)
            combined = list(set(combined))
            print(f"[i] Removed duplicates: {before - len(combined)}")

        if shuffle:
            random.shuffle(combined)
            print("[i] Shuffled combined list")

        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(combined))

        print(f"[✓] Combined wordlist saved to: {output_path}")
        return output_path


# Optional GUI integration (minimal Tkinter prompt)
def run_gui_combiner():
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox

    combiner = WordlistCombiner()
    root = tk.Tk()
    root.withdraw()

    file1 = filedialog.askopenfilename(title="Select First Wordlist", initialdir=WORDLIST_DIR)
    file2 = filedialog.askopenfilename(title="Select Second Wordlist", initialdir=WORDLIST_DIR)
    sep = simpledialog.askstring("Separator", "Enter separator (e.g., ':')", initialvalue=":")
    outname = simpledialog.askstring("Output Filename", "Enter output filename", initialvalue="combined_hybrid.txt")

    if not (file1 and file2 and sep and outname):
        messagebox.showerror("Error", "All fields are required.")
        return

    file1_name = os.path.basename(file1)
    file2_name = os.path.basename(file2)

    output = combiner.combine(file1_name, file2_name, separator=sep, output_name=outname)
    messagebox.showinfo("Success", f"Saved to {output}")


# Example usage
if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui_combiner()
    else:
        combiner = WordlistCombiner()
        output = combiner.combine('common_usernames.txt', 'simple_passwords.txt')
        print(f"Combined wordlist saved to {output}")
