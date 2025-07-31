import numpy as np
import onnxruntime as ort

class ThreatClassifier:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, vector: np.ndarray) -> str:
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        output = self.session.run(None, {self.input_name: vector.astype(np.float32)})
        prediction = output[0][0]
        return "threat" if prediction > 0.5 else "benign"
