require('dotenv').config();
const WebSocket = require('ws');
const MongoClient = require('mongodb').MongoClient;
const uri = process.env.MONGO_URI; // Ensure this is set in your environment

let ws;

function connectWebSocket() {
    const apiKey = process.env.API_KEY;
    ws = new WebSocket(`wss://atlas-mainnet.helius-rpc.com?api-key=${apiKey}`);

    ws.on('open', function open() {
        console.log('WebSocket connection established');
    });

    ws.on('message', function incoming(data) {
        handleIncomingData(data);
    });

    ws.on('close', function close() {
        console.log('WebSocket connection closed, reconnecting...');
        setTimeout(connectWebSocket, 1000);
    });

    ws.on('error', function error(err) {
        console.error('WebSocket error:', err);
    });
}

function handleIncomingData(data) {
    // Parse the incoming data and notify the appropriate user
    const parsedData = JSON.parse(data);
    const walletAddress = parsedData.walletAddress;
    const activity = parsedData.activity;

    MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true }, (err, client) => {
        if (err) throw err;
        const db = client.db('fastbot');
        const usersCollection = db.collection('users');

        usersCollection.find({ trackedWallets: walletAddress }).toArray((err, users) => {
            if (err) throw err;
            users.forEach(user => {
                notifyUser(user.client_id, activity);
            });
            client.close();
        });
    });
}

function notifyUser(chatId, activity) {
    // Logic to notify the user via Telegram bot
    console.log(`Notifying user ${chatId} about activity: ${activity}`);
    // You can use a library like axios to send a message to the Telegram bot API
}

connectWebSocket();
