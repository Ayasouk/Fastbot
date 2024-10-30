import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Telegram Bot API Key
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# MongoDB URI
MONGO_URI = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PWD')}@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority"

# Solana RPC URL
SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL')

# Moralis API Key
MORALIS_KEY_API = os.getenv('MORALIS_KEY_API')

# Encryption Key
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# WebSocket Server URL
WEBSOCKET_SERVER_URL = f"wss://atlas-mainnet.helius-rpc.com?api-key={os.getenv('API_KEY')}" 