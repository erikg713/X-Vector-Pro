# xvectorpro_vectorizer.py
import re
import hashlib
import unicodedata
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class LogVectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)

    def preprocess(self, text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip().lower()
        return text

    def fit(self, documents: list[str]):
        cleaned = [self.preprocess(doc) for doc in documents]
        self.vectorizer.fit(cleaned)

    def transform(self, documents: list[str]) -> np.ndarray:
        cleaned = [self.preprocess(doc) for doc in documents]
        return self.vectorizer.transform(cleaned).toarray()

    def fit_transform(self, documents: list[str]) -> np.ndarray:
        cleaned = [self.preprocess(doc) for doc in documents]
        return self.vectorizer.fit_transform(cleaned).toarray()
