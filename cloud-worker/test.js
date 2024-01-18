require('dotenv').config()
const { MongoClient } = require("mongodb");

const username = process.env.MONGO_USERNAME;
const password = process.env.MONGO_PWD;
if (!username || !password) {
  throw new Error('Environment variables for MongoDB credentials are not set.');
}
const uri = `mongodb+srv://${username}:${password}@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri);

const database = client.db('fastbot');
const users = database.collection('users');

const query = { client_id: process.env.TEST_CHAT_ID };
let user;
const f = async ()=>{
      user = await users.findOne(query);
      console.log("USER : ", user);
    };
f();
