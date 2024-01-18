require('dotenv').config()
const { MongoClient } = require("mongodb");

uri = "mongodb+srv://"+process.env.MONGO_USERNAME+":"+process.env.MONGO_PWD+"@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority"

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
