import telebot
from telebot import types
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ as env
from dotenv import load_dotenv
load_dotenv()
import datetime

#TODO Use Env Variable for Username and MDP
uri = "mongodb+srv://"+env['MONGO_USERNAME']+":"+env['MONGO_PWD']+"@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

telegram_api_key = env['TELEGRAM_API_KEY']

current_add = ""
bot = telebot.TeleBot(telegram_api_key)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    cid = message.chat.id
    try:
        db = client.fastbot
        users = db.users
        user = {
            "name": "Mike",
            "client_id": cid,
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
        user_id = users.insert_one(user).inserted_id
        print("User well inserted : id: "+user_id)
    except Exception as e:
        print(e)
    bot.reply_to(message, """\
Hi there, I am FastBot for Solana Trades.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.message != "answer_same":
        bot.send_message(callback.message.chat.id, "Think again...")
    if callback.data == "answer_same":
        bot.send_message(callback.message.chat.id, "🏆 Congratulations! You are the winner!")
#def echo_message(message):
#    bot.reply_to(message, message.text)

@bot.message_handler(commands=['cid'])
def handle_text(message):
    cid = message.chat.id
    bot.send_message(cid, 'Message ID is : '+str(cid))


@bot.message_handler(commands=['set'])
def handle_text(message):
    cid = message.chat.id
    # Send a ping to confirm a successful connection
    #TODO: Check if it already exists an entry or not
    msgPrice = bot.send_message(cid, 'Set your address:')
    bot.register_next_step_handler(msgPrice , step_Set_Address)

def step_Set_Address(message):
    cid = message.chat.id
    userAddress= message.text
    user = None
    try:
        db = client.fastbot
        users = db.users
        filter = {"cid":cid}
        user = users.update_one({"client_id":cid}, {"$set": {"address": userAddress}})
        print("User well updated")
        bot.send_message(cid, 'Your address is saved')
    except Exception as e:
        print(e)
    

@bot.message_handler(commands=['address'])
def handle_text(message):
    cid = message.chat.id
    try:
        db = client.fastbot
        users = db.users
        user = users.find_one({"client_id": cid})
        print("user: ", user)
        bot.send_message(cid, 'Your address is : '+str(user["address"]))
    except Exception as e:
        print(e)

@bot.message_handler(commands=['get'])
def handle_text(message):
    cid = message.chat.id
    try:
        db = client.fastbot
        users = db.users
        user = users.find_one({"client_id": cid})
        print("user: ", user)
        bot.send_message(cid, 'Your address is saved cid : '+str(user["name"]))
    except Exception as e:
        print(e)

"""
@bot.message_handler(commands=["quiz"])
def question(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    iron = types.InlineKeyboardButton('1 kilo of iron', callback_data='answer_iron')
    silver = types.InlineKeyboardButton('1 kilo of silver', callback_data='answer_silver')
    same = types.InlineKeyboardButton('Same weight', callback_data='answer_same')
    no_answer = types.InlineKeyboardButton('No answer correct', callback_data='answer_no')

    markup.add(iron, silver, same, no_answer)

    bot.send_message(message.chat.id, 'What is Lighter?', reply_markup=markup)
"""

bot.polling()

