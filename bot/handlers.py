from telebot import TeleBot
from bot.commands import track_wallet, stop_tracking_wallet, list_tracked_wallets

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['track'])
    def handle_track(message):
        track_wallet(bot, message)

    @bot.message_handler(commands=['stop'])
    def handle_stop_tracking(message):
        stop_tracking_wallet(bot, message)

    @bot.message_handler(commands=['list'])
    def handle_list_tracked_wallets(message):
        list_tracked_wallets(bot, message)

    # Add more handlers as needed 