import requests
from database.models import get_tracked_wallets
from config.settings import TELEGRAM_API_KEY

def notify_user(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Notification sent to user {chat_id}")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def handle_wallet_activity(wallet_address, activity):
    # This function should be called when there is activity on a tracked wallet
    # It should determine which users are tracking the wallet and notify them
    users_tracking_wallet = get_users_tracking_wallet(wallet_address)
    for user in users_tracking_wallet:
        message = f"Activity detected on wallet {wallet_address}: {activity}"
        notify_user(user['client_id'], message)

def get_users_tracking_wallet(wallet_address):
    # This function should query the database to find users tracking the wallet
    # For simplicity, let's assume it returns a list of users
    # You will need to implement the actual database query
    return [
        {"client_id": 123456789},  # Example user
        # Add more users as needed
    ] 