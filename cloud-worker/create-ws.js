require('dotenv').config();
const WebSocket = require('ws');

let ws;  // Variable pour conserver la référence WebSocket

function connectWebSocket() {
    ws = new WebSocket(`wss://atlas-mainnet.helius-rpc.com?api-key=$0e4e9cc8-f82d-43a8-b5f0-f5938c99d15b`);

    ws.on('open', function open() {
        console.log('WebSocket is open');
        sendRequest(ws);
    });

    ws.on('message', function incoming(data) {
        const messageStr = data.toString('utf8');
        try {
            const messageObj = JSON.parse(messageStr);
            console.log('Received:', messageObj);
    
            // Envoyer une requête HTTP à votre serveur
            axios.post(process.env.WORKER_URL, messageObj)
                 .then(response => console.log('Notification envoyée au serveur', response))
                 .catch(error => console.error('Erreur d\'envoi', error));
        } catch (e) {
            console.error('Failed to parse JSON:', e);
        }
    });

    ws.on('error', function error(err) {
        console.error('WebSocket error:', err);
    });

    ws.on('close', function close() {
        console.log('WebSocket is closed. Reconnecting...');
        setTimeout(connectWebSocket, 5000); // Reconnect after 5 seconds
    });
}

function sendRequest(ws) {
    const request = {
        jsonrpc: "2.0",
        id: 420,
        method: "transactionSubscribe",
        params: [
            {
                accountInclude: [process.env.TRACK_WALLET_1, process.env.TRACK_WALLET_2, process.env.TRACK_WALLET_3]
            },
            {
                commitment: "processed",
                encoding: "base64",
                transactionDetails: "full",
                showRewards: true,
                maxSupportedTransactionVersion: 0
            }
        ]
    };
    ws.send(JSON.stringify(request));
}

// Initier la connexion
connectWebSocket();
