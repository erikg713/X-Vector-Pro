# xvectorpro_anomaly_scoring.py
import numpy as np

class AnomalyScorer:
    def __init__(self, baseline_mean: float, baseline_std: float):
        self.mean = baseline_mean
        self.std = baseline_std

    def score(self, sample: np.ndarray) -> float:
        z = np.abs((sample.mean() - self.mean) / self.std)
        return z

    def is_anomalous(self, sample: np.ndarray, threshold: float = 3.0) -> bool:
        return self.score(sample) > threshold
