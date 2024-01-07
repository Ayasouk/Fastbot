require('dotenv').config()
const { Connection, clusterApiUrl, PublicKey } = require('@solana/web3.js');
const WebSocket = require('ws');

// Configure the Solana connection
const connection = new Connection(clusterApiUrl(process.env.MAINNET)); // Use the desired Solana network

// Replace with the wallet address you want to track
const walletAddress = new PublicKey(process.env.WALLET_ADDRESS);

// Function to set up WebSocket subscription for wallet transactions
async function trackWalletTransactions() {
  try {
    const ws = new WebSocket(connection.rpcEndpoint); // Use the desired Solana network

    ws.on('open', () => {
      console.log('WebSocket connection established.');

      // Subscribe to transaction notifications for the wallet
      const subscriptionRequest = {
        jsonrpc: '2.0',
        id: 1,
        method: 'accountSubscribe',
        params: [
            {
                commitment: 'processed', // Adjust to 'processed' for all transactions, or 'confirmed' for confirmed transactions 
                pubkey: walletAddress.toBase58(),
                encoding: 'jsonParsed',
            },
        ],
      };

      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(subscriptionRequest));
      } else {
        console.error('WebSocket is not open.');
      }
    });

    ws.on('message', (message) => {
      const response = JSON.parse(message);

      if (response.error) {
        console.error('Error in WebSocket message:', response.error);
        return;
      }
      if (response.method === 'accountNotification') {
        const transaction = response.params.result.value;
        console.log('Received transaction:', transaction);
        // You can further process or analyze the transaction data here
      }
    });

    ws.on('close', () => {
      console.log('WebSocket connection closed.');
    });

    ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  } catch (error) {
    console.error('Error setting up WebSocket:', error);
    // Consider adding reconnection logic or cleanup here
  }
}

// Call the function to start tracking wallet transactions
trackWalletTransactions();
