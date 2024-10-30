from pymongo import MongoClient
from config.settings import MONGO_URI

# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client.fastbot
users_collection = db.users

def add_tracked_wallet(chat_id, wallet_address):
    users_collection.update_one(
        {"client_id": chat_id},
        {"$addToSet": {"trackedWallets": {"address": wallet_address, "status": "active"}}},
        upsert=True
    )

def remove_tracked_wallet(chat_id, wallet_address):
    users_collection.update_one(
        {"client_id": chat_id},
        {"$pull": {"trackedWallets": {"address": wallet_address}}}
    )

def get_tracked_wallets(chat_id):
    user = users_collection.find_one({"client_id": chat_id})
    if user and "trackedWallets" in user:
        return [wallet["address"] for wallet in user["trackedWallets"]]
    return []

def pause_tracked_wallet(chat_id, wallet_address):
    users_collection.update_one(
        {"client_id": chat_id, "trackedWallets.address": wallet_address},
        {"$set": {"trackedWallets.$.status": "paused"}}
    )

def resume_tracked_wallet(chat_id, wallet_address):
    users_collection.update_one(
        {"client_id": chat_id, "trackedWallets.address": wallet_address},
        {"$set": {"trackedWallets.$.status": "active"}}
    )