import requests
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64

PI_API_BASE_URL = "https://api.minepi.com/v2"

class PiNetworkClient:
    def __init__(self, app_id: str, api_key: str, api_secret: str):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_headers(self):
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_payment(self, user_uid: str, amount: float, memo: str, metadata: dict):
        payload = {
            "amount": amount,
            "memo": memo,
            "metadata": metadata,
            "uid": user_uid
        }

        response = requests.post(
            f"{PI_API_BASE_URL}/payments",
            json=payload,
            headers=self._get_headers()
        )
        return response.json()

    def complete_payment(self, payment_id: str, txid: str):
        response = requests.post(
            f"{PI_API_BASE_URL}/payments/{payment_id}/complete",
            json={"txid": txid},
            headers=self._get_headers()
        )
        return response.json()

    def verify_webhook_signature(self, raw_body: bytes, x_signature: str):
        expected_sig = hmac.new(
            self.api_secret.encode(),
            msg=raw_body,
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_sig, x_signature)
load_dotenv()

class PiNetwork:
    def __init__(self):
        self.api_key = None
        self.wallet_seed = None
        self.network = None

    def initialize(self, api_key: str = None, wallet_private_seed: str = None, network: str = None):
        self.api_key = api_key or os.getenv("PI_API_KEY")
        self.wallet_seed = wallet_private_seed or os.getenv("PI_WALLET_SEED")
        self.network = network or os.getenv("PI_NETWORK")

    def _headers(self):
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_payment(self, payment_data: dict) -> str:
        response = requests.post(
            f"https://api.minepi.com/v2/payments",
            json=payment_data,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get("identifier")

    def submit_payment(self, payment_id: str, pending_payments: bool = False) -> str:
        response = requests.post(
            f"https://api.minepi.com/v2/payments/{payment_id}/submit",
            json={"pending_payments": pending_payments},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get("txid")

    def complete_payment(self, payment_id: str, txid: str) -> dict:
        response = requests.post(
            f"https://api.minepi.com/v2/payments/{payment_id}/complete",
            json={"txid": txid},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_payment(self, payment_id: str) -> dict:
        response = requests.get(
            f"https://api.minepi.com/v2/payments/{payment_id}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def cancel_payment(self, payment_id: str) -> dict:
        response = requests.post(
            f"https://api.minepi.com/v2/payments/{payment_id}/cancel",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_incomplete_server_payments(self) -> list:
        response = requests.get(
            "https://api.minepi.com/v2/payments/incomplete_server_payments",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
 