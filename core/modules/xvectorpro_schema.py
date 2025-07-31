# xvectorpro_schema.py
from dataclasses import dataclass
from typing import List

@dataclass
class VectorInput:
    raw_text: str
    source: str
    timestamp: str

@dataclass
class VectorOutput:
    vector: List[float]
    threat_label: str
    anomaly_score: float
