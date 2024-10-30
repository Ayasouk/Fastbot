require('dotenv').config()
var myHeaders = new Headers();
myHeaders.append("x-api-key", process.env.SHYFT_API_KEY);
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "network": "mainnet-beta",
  "addresses": [
    process.env.TRACK_WALLET_1,
    process.env.TRACK_WALLET_2,
    process.env.TRACK_WALLET_3
  ],
  "callback_url": "https://test-shyft-1.kachou-help.workers.dev",
  "events": [
    "SWAP",
    "SOL_TRANSFER"
  ],
  "enable_raw":true,
  "enable_events":true,
  "type":"CALLBACK",
  "encoding":"RAW"
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("https://api.shyft.to/sol/v1/callback/create", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));