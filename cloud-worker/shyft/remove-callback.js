require('dotenv').config()

var myHeaders = new Headers();
myHeaders.append("x-api-key", process.env.SHYFT_API_KEY);
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
    "id": "ID_CALLBACK_HERE",
});

var requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("https://api.shyft.to/sol/v1/callback/remove", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));