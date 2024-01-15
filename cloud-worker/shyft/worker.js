/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run "npm run dev" in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run "npm run deploy" to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

const TELEGRAM_BOT_TOKEN = BOT_TOKEN;
const TELEGRAM_CHAT_ID = CHAT_ID;
const SHYFT_API_KEY=API_KEY;
const SHYFT_RPC_URL = `https://rpc.shyft.to?api_key=${SHYFT_API_KEY}`;

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  if (request.method === 'POST') {
    try {
      const requestBody = await request.json();
      console.log('Received POST request with body:', requestBody);
          //THIS IS FOR TRANSFER UPDATES (comment this section out if you are doing something else)
      // Extract transaction description, timestamp, signature
      //const Transfertimestamp = new Date(requestBody[0].timestamp * 1000).toLocaleString(); // Convert Unix timestamp to readable date-time
      const Transfertimestamp = requestBody.timestamp; // Convert Unix timestamp to readable date-time
      //const Transfersignature = `https://xray.helius.xyz/tx/${requestBody[0].signature}`
      const action = requestBody["actions"][0].type;
      //TODO: Adapt the code if it's SWAP or SOL_TRANSFER
      let tokenInSymbol;
      let tokenOutSymbol;
      let tokenInAddress;
      let tokenOutAddress;
      let tokenInAmount;
      let tokenOutAmount
      let messageToSendTransfer;

      if(action==="SWAP"){
        tokenInSymbol = requestBody["actions"][0]["info"]["tokens_swapped"]["in"]["symbol"]
        tokenOutSymbol = requestBody["actions"][0]["info"]["tokens_swapped"]["out"]["symbol"]
        tokenInAddress = requestBody["actions"][0]["info"]["tokens_swapped"]["in"]["token_address"]
        tokenOutAddress = requestBody["actions"][0]["info"]["tokens_swapped"]["out"]["token_address"]
        tokenInAmount = requestBody["actions"][0]["info"]["tokens_swapped"]["in"]["amount"]
        tokenOutAmount = requestBody["actions"][0]["info"]["tokens_swapped"]["out"]["amount"]
          // Construct the message
        messageToSendTransfer = 
        `----NEW UPDATE---\n`+
        `Type:\n${action}\n`+
        `Timestamp:\n${Transfertimestamp}\n`+
        `Swapped IN:  ${tokenInAmount} ${tokenInSymbol} : ${tokenInAddress}\n`+
        `FOR OUT: ${tokenOutAmount} ${tokenOutSymbol} : ${tokenOutAddress}\n`;
      } else {
        messageToSendTransfer = 
        `----NEW UPDATE---\n`+
        `Type:\n${action}\n`+
        `Timestamp:\n${Transfertimestamp}\n`;
      }
      await sendToTelegramTransfer(messageToSendTransfer); // Send to Telegram

    } catch (error) {
      console.error('Error parsing JSON:', error);
      return new Response('Bad request body.', {status: 400});
    }


    return new Response('Logged POST request body.', {status: 200});
  } else {
    return new Response('Method not allowed.', {status: 405});
  }
}

// This function is used to send NFT Updates to the bot
async function sendToTelegramNFT(message, imageUrl) {
  const telegramUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto`;
  const response = await fetch(telegramUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      photo: imageUrl,
      caption: message,
      parse_mode: "HTML"
    }),
  });
  const responseData = await response.json();

  if (!response.ok) {
    console.error('Failed to send photo to Telegram:', responseData);
  }
}



//This function is used to send Transfer Updates to the Bot
async function sendToTelegramTransfer(message) {
  const telegramUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const response = await fetch(telegramUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      text: message, 
      parse_mode: "HTML"
    }),
  });
  const responseData = await response.json();

  if (!response.ok) {
    console.error('Failed to send message to Telegram:', responseData);
  }
}


//This function gets images associated to NFTs that are features in updates.
async function getAssetImageUrl(mintAddress) {
  const response = await fetch(SHYFT_RPC_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 'my-id',
      method: 'getAsset',
      params: {
        id: mintAddress,
      },
    }),
  });
  const { result } = await response.json();
  return result.content.links.image;
}