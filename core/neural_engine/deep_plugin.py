# core/neural_engine/deep_plugin.py

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset

class DeepModel(nn.Module):
    def __init__(self, input_size, hidden_dim=128, output_size=3):
        super(DeepModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, output_size)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


class DeepLearningEngine:
    def __init__(self, model_path="models/deep_model.pt", input_size=8, device=None):
        self.model_path = model_path
        self.input_size = input_size
        self.output_size = 3  # 'benign', 'suspicious', 'malicious'
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.label_encoder = LabelEncoder()
        self.model = DeepModel(input_size=input_size, output_size=self.output_size).to(self.device)
        self.trained = False
        self.load_model()

    def train(self, X, y, epochs=15, batch_size=32, lr=0.001):
        y_encoded = self.label_encoder.fit_transform(y)
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y_encoded, dtype=torch.long)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        self.model.train()
        for epoch in range(epochs):
            for batch_x, batch_y in loader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                optimizer.zero_grad()
                output = self.model(batch_x)
                loss = criterion(output, batch_y)
                loss.backward()
                optimizer.step()

        self.trained = True
        self.save_model()

    def predict(self, features):
        if not self.trained:
            return "monitor"
        try:
            self.model.eval()
            with torch.no_grad():
                input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(self.device)
                logits = self.model(input_tensor)
                pred = torch.argmax(logits, dim=1).cpu().item()
                label = self.label_encoder.inverse_transform([pred])[0]
                return {
                    "benign": "monitor",
                    "suspicious": "alert",
                    "malicious": "isolate"
                }.get(label, "monitor")
        except:
            return "monitor"

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        torch.save({
            'model_state': self.model.state_dict(),
            'label_encoder': self.label_encoder.classes_.tolist()
        }, self.model_path)

    def load_model(self):
        if os.path.exists(self.model_path):
            checkpoint = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state'])
            self.label_encoder.classes_ = np.array(checkpoint['label_encoder'])
            self.trained = True
