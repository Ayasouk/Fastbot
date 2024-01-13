require('dotenv').config()
var myHeaders = new Headers();
myHeaders.append("x-api-key", process.env.SHYFT_API_KEY);
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "network": "devnet",
  "addresses": [
    ADRESSES_TO_TRACK_1
  ],
  "callback_url": "YOUR CALLBACK URL",
  "events": [
    "SWAP",
    "SOL_TRANSFER"
  ]
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