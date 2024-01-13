require('dotenv').config()

var myHeaders = new Headers();
myHeaders.append("x-api-key", process.env.SHYFT_API_KEY);

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  redirect: 'follow'
};

fetch("https://api.shyft.to/sol/v1/callback/list", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));