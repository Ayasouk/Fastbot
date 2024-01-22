require('dotenv').config();
const fernet = require('fernet');
const { MongoClient } = require("mongodb");
const web3 = require('@solana/web3.js');
const bs58 = require('bs58');

const username = process.env.MONGO_USERNAME;
const password = process.env.MONGO_PWD;
const clientId = process.env.TEST_CHAT_ID;

if (!username || !password) {
  throw new Error('Environment variables for MongoDB credentials are not set.');
}
const uri = `mongodb+srv://${username}:${password}@cluster0.b5ojrgn.mongodb.net/?retryWrites=true&w=majority`;

// Connect to the MongoDB cluster
const client = new MongoClient(uri);
const database = client.db(process.env.DB_NAME);
const users = database.collection('users');

// Connect to web3
const connection = new web3.Connection(HELIUS_RPC_URL, 'confirmed');

console.log("CLIENT ID : ", clientId);
if (!clientId) {
  throw new Error('TEST_CHAT_ID environment variable is not set.');
}
const query = { client_id: parseInt(clientId) };;
const executeTransfer = async () => {
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
  let pkey = token.decode();
  pkey = Uint8Array(bs58.decode(pkey));

  const account = web3.Keypair.fromSecretKey(pkey);
  const account2 = web3.Keypair.fromSecretKey(pkey);
  console.log("PKEY : ", pkey);

  // Test Transfer between two accounts
  (async () => {
    const transaction = new web3.Transaction().add(
     web3.SystemProgram.transfer({
       fromPubKey: account.publicKey,
       toPubKey: account2.publicKey,
       lamports: web3.LAMPORTS_PER_SOL * 0.001,
     }),
    );
    const signature = await web3.sendAndConfirmTransaction(
     connection,
     transaction,
     [account],
    );
 })();
};
executeTransfer();
