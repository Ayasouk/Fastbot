from telebot import TeleBot
from database.models import add_tracked_wallet, remove_tracked_wallet, get_tracked_wallets
from websocket.manager import update_websocket

def track_wallet(bot: TeleBot, message):
    try:
        wallet_address = message.text.split(' ')[1]
        chat_id = message.chat.id
        
        # Add wallet to the user's tracked list in the database
        add_tracked_wallet(chat_id, wallet_address)
        
        # Update the WebSocket configuration
        update_websocket(wallet_address)
        
        bot.send_message(chat_id, f"Started tracking wallet: {wallet_address}")
    except Exception as e:
        bot.send_message(chat_id, f"Error tracking wallet: {e}")

def stop_tracking_wallet(bot: TeleBot, message):
    try:
        wallet_address = message.text.split(' ')[1]
        chat_id = message.chat.id
        
        # Remove wallet from the user's tracked list in the database
        remove_tracked_wallet(chat_id, wallet_address)
        
        # Update the WebSocket configuration
        update_websocket(wallet_address, remove=True)
        
        bot.send_message(chat_id, f"Stopped tracking wallet: {wallet_address}")
    except Exception as e:
        bot.send_message(chat_id, f"Error stopping tracking of wallet: {e}")

def list_tracked_wallets(bot: TeleBot, message):
    try:
        chat_id = message.chat.id
        wallets = get_tracked_wallets(chat_id)
        
        if wallets:
            response = "Tracked Wallets:\n" + "\n".join(wallets)
        else:
            response = "No wallets are currently being tracked."
        
        bot.send_message(chat_id, response)
    except Exception as e:
        bot.send_message(chat_id, f"Error listing tracked wallets: {e}")

@bot.message_handler(commands=['stop'])
def handle_stop_tracking(message):
    stop_tracking_wallet(bot, message)

@bot.message_handler(commands=['list'])
def handle_list_tracked_wallets(message):
    list_tracked_wallets(bot, message)