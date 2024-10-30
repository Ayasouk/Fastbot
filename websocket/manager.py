import json
import os
import requests
from config.settings import WEBSOCKET_SERVER_URL

def update_websocket(wallet_address, remove=False):
    try:
        action = "remove" if remove else "add"
        payload = {
            "action": action,
            "wallet_address": wallet_address
        }
        
        response = requests.post(WEBSOCKET_SERVER_URL, json=payload)
        
        if response.status_code == 200:
            print(f"Successfully updated WebSocket for {action}ing wallet: {wallet_address}")
        else:
            print(f"Failed to update WebSocket: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error updating WebSocket: {e}") 