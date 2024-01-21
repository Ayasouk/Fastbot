require('dotenv').config();
const fernet = require('fernet');
const { MongoClient } = require("mongodb");

const username = process.env.MONGO_USERNAME;
const password = process.env.MONGO_PWD;
const clientId = process.env.TEST_CHAT_ID;
if (!username || !password) {
  throw new Error('Environment variables for MongoDB credentials are not set.');
}
const uri = `mongodb+srv://${username}:${password}@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri);

const database = client.db(process.env.DB_NAME);
const users = database.collection('users');

console.log("CLIENT ID : ", clientId);
if (!clientId) {
  throw new Error('TEST_CHAT_ID environment variable is not set.');
}
const query = { client_id: parseInt(clientId) };;
const findUser = async () => {
  const user = await users.findOne(query);
  if (!user) {
    console.error('User not found.');
    return;
  }
  console.log("USER : ", user);

  const secret = new fernet.Secret(process.env.ENCRYPTION_KEY);

  var token = new fernet.Token({
    secret: secret,
    token: user.pkey,
    ttl: 0
  })
  const pkey = token.decode();
  console.log("PKEY : ", pkey);
  /*
  "Message"
  */
};
findUser();
