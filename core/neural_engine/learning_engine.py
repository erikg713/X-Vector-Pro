# core/neural_engine/learning_engine.py

import os
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from core.neural_engine.deep_plugin import DeepLearningEngine


class LearningEngine:
    def __init__(self, mode="deep", model_dir="models"):
        self.mode = mode.lower()  # 'deep' or 'rf'
        self.model_dir = model_dir
        self.rf_model_path = os.path.join(model_dir, "rf_model.pkl")
        self.deep_model = DeepLearningEngine(model_path=os.path.join(model_dir, "deep_model.pt"))
        self.rf_model = None
        self.label_encoder = LabelEncoder()
        self.trained = False

        os.makedirs(model_dir, exist_ok=True)
        if self.mode == "rf":
            self._load_rf_model()
        else:
            self.deep_model.load_model()

    def _load_rf_model(self):
        if os.path.exists(self.rf_model_path):
            with open(self.rf_model_path, "rb") as f:
                data = joblib.load(f)
                self.rf_model = data["model"]
                self.label_encoder.classes_ = data["classes"]
                self.trained = True
        else:
            self.rf_model = RandomForestClassifier(n_estimators=100)

    def train(self, data, labels):
        labels = [str(lbl).lower() for lbl in labels]
        X = np.array(data)
        y = self.label_encoder.fit_transform(labels)

        if self.mode == "rf":
            self.rf_model.fit(X, y)
            joblib.dump({
                "model": self.rf_model,
                "classes": self.label_encoder.classes_
            }, self.rf_model_path)
            self.trained = True
        else:
            self.deep_model.train(X, labels)
            self.trained = True

    def select_action(self, features):
        if self.mode == "rf":
            return self._rf_predict(features)
        else:
            return self.deep_model.predict(features)

    def _rf_predict(self, features):
        if not self.trained or self.rf_model is None:
            return "monitor"
        try:
            pred = self.rf_model.predict([features])[0]
            label = self.label_encoder.inverse_transform([pred])[0]
            return {
                "benign": "monitor",
                "suspicious": "alert",
                "malicious": "isolate"
            }.get(label, "monitor")
        except:
            return "monitor"

    def set_mode(self, mode):
        self.mode = mode.lower()
        if self.mode == "rf":
            self._load_rf_model()
        else:
            self.deep_model.load_model()

    def export_config(self, path="models/config.json"):
        with open(path, "w") as f:
            json.dump({"mode": self.mode}, f)

    def import_config(self, path="models/config.json"):
        if os.path.exists(path):
            with open(path, "r") as f:
                config = json.load(f)
                self.set_mode(config.get("mode", "rf"))
