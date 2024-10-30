import telebot
from config.settings import TELEGRAM_API_KEY
from bot.handlers import register_handlers

# Initialize the bot with the Telegram API key
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Register command handlers
register_handlers(bot)

if __name__ == "__main__":
    print("Bot is running...")
    # Start polling for updates
    bot.polling(none_stop=True) 