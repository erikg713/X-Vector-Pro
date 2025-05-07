from pymongo import MongoClient
from utils.logger import log

def get_recon_history(limit=20):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["xvector"]
        col = db["auto_recon"]
        history = list(col.find().sort("timestamp", -1).limit(limit))
        return history
    except Exception as e:
        log(f"[!] Failed to retrieve recon history: {e}")
        return []
