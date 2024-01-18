import telebot
from telebot import types
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ as env
from dotenv import load_dotenv
import asyncio
#from pyserum import market
import solana
from solana.rpc.api import Client, Pubkey
from solders.pubkey import Pubkey
from moralis import sol_api
from cryptography.fernet import Fernet
from pymongo import MongoClient
import os
load_dotenv()
import datetime


api_key = env['MORALIS_KEY_API']

#TODO Use Env Variable for Username and MDP
uri = "mongodb+srv://"+env['MONGO_USERNAME']+":"+env['MONGO_PWD']+"@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority"
rpc_url = env['SOLANA_RPC_URL']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.fastbot
users_collection = db.users

solana_client = Client(rpc_url)

telegram_api_key = env['TELEGRAM_API_KEY']

# Encryption key (should be stored securely, not like this)
encryption_key = env['ENCRYPTION_KEY']
cipher_suite = Fernet(encryption_key)


current_add = ""
bot = telebot.TeleBot(telegram_api_key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt(encrypted_text, encryption_key):
    """ Decrypt the text using Fernet symmetric encryption """
    cipher_suite = Fernet(encryption_key)
    try:
        decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
        return decrypted_text
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return None

def update_user_private_key(chat_id, encrypted_key):
    users_collection.update_one({"client_id": chat_id}, {"$set": {"pkey": encrypted_key}}, upsert=True)


# Set p key
@bot.message_handler(commands=['setSigner'])
def set_signer(message):
    cid = message.chat.id
    try:
        # Get the wallet address from the message text
        signer_key = message.text.split()[1]
        # Encrypt the p key
        encrypted_key = encrypt_data(signer_key)
        # Add the p key into the database
        update_user_private_key(cid, encrypted_key)
        bot.send_message(cid, "Your wallet as been securely set")
        
    except Exception as e:
        bot.reply_to(message, "Error fetching transactions: " + str(e))


# Get last transactions of a given wallet
@bot.message_handler(commands=['lasttransactions'])
def get_last_transactions(message):
    cid = message.chat.id
    try:
        # Get the wallet address from the message text
        wallet_address = message.text.split()[1]

        # Retrieve the last 5 transactions for the wallet
        transactions = solana_client.get_signatures_for_address(
                        Pubkey.from_string(wallet_address),
                        limit = 5 # Specify how much last transactions to fetch
                        )
        #transactions = solana_client.get_account_transactions(wallet_address, limit=5)

        # Format and send the transactions as a reply
        #bot.send_message(cid, "Transactions retrieved : "+str(transactions.value[1].signature))
        
        if transactions:
            response = "Last 5 transactions for wallet address:\n"
            for tx in transactions.value:
                response += f"Transaction ID: {tx.signature} \n"
                response += f"Block Number: {tx.slot} \n"
                response += f"Timestamp: {tx.block_time} \n"
            response += "\n"
        else:
            response = "No transactions found for the wallet address."

        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, "Error fetching transactions: " + str(e))


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

# Get balance
@bot.message_handler(commands=['balance'])
def handle_text(message):
    cid = message.chat.id
    address = message.text.split(' ')[1]
    params = {
    "network": "mainnet",
    "address": address
    }
    result = sol_api.account.balance(
        api_key=api_key,
        params=params,
    )

    bot.send_message(cid, f'the balance of {address} is {result["solana"]} sol')



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


async def task2(cid):
    i = 0
    while i < 10:
        try:
            bot.send_message(cid, f'Message n°{cid} - {i}')

            await asyncio.sleep(10)
            i+=1
        except Exception as e:
            print(f'Error in task2: {e}')

@bot.message_handler(commands=['track'])
def handle_track(message):
    cid = message.chat.id
    asyncio.run(task2(cid))


@bot.message_handler(commands=['listtokens'])
def list_tokens(message):
    cid = message.chat.id
    user_message = message.text.split()
    
    if len(user_message) != 2:
        bot.send_message(cid, "Please provide a Solana address with the command.")
        return
    print('user acc : '+user_message[1])
    solana_address = Pubkey.from_string(user_message[1])
    
    try:
        # Fetch the token balances for the given Solana address
        token_balances = solana_client.get_token_account_balance(solana_address)
        
        if not token_balances:
            bot.send_message(cid, "No token balances found for the provided Solana address.")
            return

        response = "Token Balances:\n"
        
        for balance in token_balances:
            token_address = balance['account']['data']['parsed']['info']['mint']
            token_balance = balance['account']['data']['parsed']['info']['tokenAmount']['amount']
            
            # Fetch the token symbol or name using the token address
            token_info = solana_client.get_token_info(token_address)
            token_symbol = token_info['symbol']
            
            response += f"{token_symbol}: {token_balance}\n"

        bot.send_message(cid, response)
    except Exception as e:
        bot.send_message(cid, f"Error fetching token balances: {e}")


@bot.message_handler(commands=["menu"])
def question(message):
        user = users_collection.find_one({"client_id": message.chat.id})
        menu_str=f'----------MENU------------\n'
        menu_str+=f'ADDRESS: { user["address"] if user["address"] else "Not Set"}\n'
        menu_str+=f'SLIPPAGE: {user["slippage"] if "slippage" in user.keys() else "Not Set"}\n'
        menu_str+=f'MAX GAS FEE: {user["maxgas"] if "maxgas" in user.keys() else "Not Set"}\n'
        menu_str+=f'PERCENTAGE BUY: {user["percentage"] if "percentage" in user.keys() else "Not Set"}\n'
        
        markup = types.InlineKeyboardMarkup(row_width=2)

        slippage = types.InlineKeyboardButton('Set Slippage Tolerance', callback_data='answer_slippage')
        gas = types.InlineKeyboardButton('Set Max Gas Fees', callback_data='answer_gas')
        buy = types.InlineKeyboardButton('Set Percentage to Buy', callback_data='answer_buy')

        markup.add(slippage, gas, buy)
 
        bot.send_message(message.chat.id, menu_str, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
        if call.message:
            if call.data == "answer_slippage":
                bot.send_message(call.message.chat.id, 'Enter the slippage tolerance you want to set')
                bot.register_next_step_handler(call.message, set_slippage)
            elif call.data == "answer_gas":
                bot.send_message(call.message.chat.id, 'Enter the max gas fees you want to set')
                bot.register_next_step_handler(call.message, set_max_gas)
            elif call.data == "answer_buy":
                bot.send_message(call.message.chat.id, 'Enter the percentage you want to buy')
                bot.register_next_step_handler(call.message, set_percentage)
            else:
                bot.send_message(call.message.chat.id, 'Unknown command')
            return
        else:
            bot.send_message(call.message.chat.id, 'Unknown command')
            return
        
def set_slippage(message):
        try:
            if not message.text.replace('.', '', 1).isdigit():
+               bot.send_message(message.chat.id, 'Please enter a valid number for percentage')
+               return
            slippage = float(message.text)
            if slippage < 0 or slippage > 100:
                bot.send_message(message.chat.id, 'Slippage must be between 0 and 100')
                return
            users_collection.update_one({"client_id": message.chat.id}, {"$set": {"slippage": slippage}})
            bot.send_message(message.chat.id, f'Slippage tolerance set to {slippage}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error setting slippage: {e}')
    
def set_max_gas(message):
        try:
            if not message.text.replace('.', '', 1).isdigit():
                bot.send_message(message.chat.id, 'Please enter a valid number for percentage')
                return
            max_gas = float(message.text)
            if max_gas < 0:
                bot.send_message(message.chat.id, 'Max gas must be greater than 0')
                return
            users_collection.update_one({"client_id": message.chat.id}, {"$set": {"maxgas": max_gas}})
            bot.send_message(message.chat.id, f'Max gas fees set to {max_gas}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error setting max gas: {e}')
    
def set_percentage(message):
        try:
            if not message.text.replace('.', '', 1).isdigit():
                bot.send_message(message.chat.id, 'Please enter a valid number for percentage')
                return
            percentage = float(message.text)
            if percentage < 0 or percentage > 100:
                bot.send_message(message.chat.id, 'Percentage must be between 0 and 100')
                return
            users_collection.update_one({"client_id": message.chat.id}, {"$set": {"percentage": percentage}})
            bot.send_message(message.chat.id, f'Percentage to buy set to {percentage}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error setting percentage: {e}')
    


bot.polling()

