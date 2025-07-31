import os

class ModelLoader:
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = model_dir

    def list_models(self) -> list[str]:
        return [f for f in os.listdir(self.model_dir) if f.endswith(".onnx")]

    def get_model_path(self, model_name: str) -> str:
        return os.path.join(self.model_dir, model_name)
