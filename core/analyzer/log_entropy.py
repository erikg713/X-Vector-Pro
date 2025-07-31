import math
from collections import Counter

class LogEntropyAnalyzer:
    def __init__(self, base=2):
        self.base = base

    def shannon_entropy(self, data: str) -> float:
        if not data:
            return 0.0
        counter = Counter(data)
        total = len(data)
        return -sum((count / total) * math.log(count / total, self.base) for count in counter.values())

    def analyze_log(self, log: str, threshold: float = 4.5) -> bool:
        entropy = self.shannon_entropy(log)
        return entropy > threshold  # High entropy may indicate obfuscation or encoded payloads

# Example usage
if __name__ == "__main__":
    analyzer = LogEntropyAnalyzer()
    log_sample = "aHR0cDovL2V2aWwubmV0L2NnaS1iaW4vc2hlbGw="
    print("Entropy:", analyzer.shannon_entropy(log_sample))
    print("Suspicious:", analyzer.analyze_log(log_sample))
