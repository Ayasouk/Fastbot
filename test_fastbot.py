import unittest
from fastbot import encrypt_data, decrypt, update_user_private_key, set_signer, get_last_transactions, get_token_price

class TestFastbot(unittest.TestCase):

    def test_encrypt_data(self):
        # Test that data is correctly encrypted
        print("TEST ENCRYPT DATA")
        expectedResult="gAAAAABlsBtGAAECAwQFBgcICQoLDA0ODxpYaYvSK7xuFaRvgTOKGJ-YGLvQCU50eqbe7pBz9uScXxHgEpj0qUErd1i1c-LW7w=="
        msg = "Message Test"
        encryptedMsg = encrypt_data(msg)
        self.assertNotEqual(msg, encryptedMsg)
        pass

    def test_decrypt(self):
        # Test that encrypted data is correctly decrypted
        print("DECRYPT DATA")
        expectedResult = "Message Test"
        encryptedMsg="gAAAAABlsBtGAAECAwQFBgcICQoLDA0ODxpYaYvSK7xuFaRvgTOKGJ-YGLvQCU50eqbe7pBz9uScXxHgEpj0qUErd1i1c-LW7w=="
        msg = decrypt(encryptedMsg)
        self.assertEqual(expectedResult, msg)
        pass

    def test_update_user_private_key(self):
        # Test that the user's private key is correctly updated in the database
        pass

    def test_set_signer(self):
        # Test the '/setSigner' command handler
        pass

    def test_get_last_transactions(self):
        # Test the '/lasttransactions' command handler
        pass

    def test_get_token_price(self):
        # Test that the token price is correctly retrieved
        pass

if __name__ == '__main__':
    unittest.main()