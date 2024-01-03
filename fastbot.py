import telebot
from telebot import types
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ as env
from dotenv import load_dotenv
#from pyserum import market
import solana
from solana.rpc.api import Client

load_dotenv()
import datetime

#TODO Use Env Variable for Username and MDP
uri = "mongodb+srv://"+env['MONGO_USERNAME']+":"+env['MONGO_PWD']+"@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority"
rpc_url = "https://api.mainnet-beta.solana.com"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
solana_client = Client(rpc_url)

telegram_api_key = env['TELEGRAM_API_KEY']

current_add = ""
bot = telebot.TeleBot(telegram_api_key)

# Get token price 
def get_token_price(market_address, token_address):
    # Fetch the order book for the market
    orderbook_data = solana_client.get_orderbook(market_address)

    if not orderbook_data:
        return None

    bids, asks = orderbook_data['bids'], orderbook_data['asks']

    # Find the price for the token you're interested in
    for bid in bids:
        if bid[0] == token_address:
            price = bid[1]
            return price

    for ask in asks:
        if ask[0] == token_address:
            price = ask[1]
            return price

    return None

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

# Getting the conversation id
@bot.message_handler(commands=['cid'])
def handle_text(message):
    cid = message.chat.id
    bot.send_message(cid, 'Message ID is : '+str(cid))

# Set an address to track
@bot.message_handler(commands=['set'])
def handle_text(message):
    cid = message.chat.id
    # Send a ping to confirm a successful connection
    #TODO: Check if it already exists an entry or not
    msgPrice = bot.send_message(cid, 'Set your address:')
    bot.register_next_step_handler(msgPrice , step_Set_Address)
# Getting the address
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
    
# Showing the address set
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

# Getting user info
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

@bot.message_handler(commands=['tokenprice'])
def handle_token_price(message):
    cid = message.chat.id
    try:
        token_address = message.text.split(' ')[1]

        market_address = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

        token_price = get_token_price(market_address, token_address)

        if token_price is not None:
            bot.send_message(cid, f'The price of {token_address} is {token_price} USD')
        else:
            bot.send_message(cid, "The price isn't found")
    except Exception as e:
        print(e)
        bot.send_message(cid, 'Error fetching token price. Please try again.')
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

