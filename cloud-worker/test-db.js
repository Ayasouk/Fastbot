require('dotenv').config();
require('fernet');
const { MongoClient } = require("mongodb");

const username = process.env.MONGO_USERNAME;
const password = process.env.MONGO_PWD;
if (!username || !password) {
  throw new Error('Environment variables for MongoDB credentials are not set.');
}
const uri = `mongodb+srv://${username}:${password}@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri);

const database = client.db(process.env.DB_NAME);
const users = database.collection('users');

const clientId = process.env.TEST_CHAT_ID;
if (!clientId) {
  throw new Error('TEST_CHAT_ID environment variable is not set.');
}
const query = { client_id: clientId };
const findUser = async () => {
  const user = await users.findOne(query);
  if (!user) {
    console.error('User not found.');
    return;
  }
  console.log("USER : ", user);
  var token = new fernet.Token({
    secret: process.env.ENCRYPTION_KEY,
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
f();
