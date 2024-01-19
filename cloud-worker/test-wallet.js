const { Connection, Transaction, PublicKey, SystemProgram, sendAndConfirmTransaction } = require('@solana/web3.js');
const { Keypair } = require('solana-web3.js');

// Define your Solana network connection
const connection = new Connection('https://api.mainnet-beta.solana.com');

// Define your wallet private key as a Buffer
const privateKeyBuffer = Buffer.from('YOUR_PRIVATE_KEY', 'base64'); // Replace with your private key

// Create a Solana wallet from the private key
const wallet = new Keypair(privateKeyBuffer);

// Define the token to swap (source token)
const sourceTokenAccount = new PublicKey('YOUR_SOURCE_TOKEN_ACCOUNT_ADDRESS'); // Replace with the source token account address
const sourceTokenMint = new PublicKey('TOKEN_MINT_ADDRESS'); // Replace with the source token mint address

// Define the destination token account
const destinationTokenAccount = new PublicKey('YOUR_DESTINATION_TOKEN_ACCOUNT_ADDRESS'); // Replace with the destination token account address

// Define the amount to swap (in lamports)
const amountToSwap = 100000000; // Replace with the amount you want to swap (e.g., 1 SOL)

// Build the transaction
const transaction = new Transaction().add(
  SystemProgram.transfer({
    fromPubkey: wallet.publicKey,
    toPubkey: sourceTokenAccount,
    lamports: amountToSwap,
  }),
);

// Sign the transaction
transaction.sign(wallet);

(async () => {
  try {
    // Send and confirm the transaction
    const signature = await sendAndConfirmTransaction(connection, transaction);

    console.log(`Transaction confirmed. Signature: ${signature}`);
  } catch (error) {
    console.error('Error swapping tokens:', error);
  }
})();
