'''Tests string operations.'''

import struct
import unittest

import rsa
from rsa import pkcs1

class BinaryTest(unittest.TestCase):

    def setUp(self):
        (self.pub, self.priv) = rsa.newkeys(256)

    def test_enc_dec(self):

        message = struct.pack('>IIII', 0, 0, 0, 1)
        print("\tMessage:   %r" % message)

        encrypted = pkcs1.encrypt(message, self.pub)
        print("\tEncrypted: %r" % encrypted)

        decrypted = pkcs1.decrypt(encrypted, self.priv)
        print("\tDecrypted: %r" % decrypted)

        self.assertEqual(message, decrypted)

    def test_decoding_failure(self):

        message = struct.pack('>IIII', 0, 0, 0, 1)
        encrypted = pkcs1.encrypt(message, self.pub)

        # Alter the encrypted stream
        encrypted = encrypted[:5] + chr(ord(encrypted[5]) + 1) + encrypted[6:]
        
        self.assertRaises(pkcs1.DecryptionError, pkcs1.decrypt, encrypted,
                          self.priv)

    def test_randomness(self):
        '''Encrypting the same message twice should result in different
        cryptos.
        '''
        
        message = struct.pack('>IIII', 0, 0, 0, 1)
        encrypted1 = pkcs1.encrypt(message, self.pub)
        encrypted2 = pkcs1.encrypt(message, self.pub)
        
        self.assertNotEqual(encrypted1, encrypted2)

class SignatureTest(unittest.TestCase):

    def setUp(self):
        (self.pub, self.priv) = rsa.newkeys(512)

    def test_sign_verify(self):
        '''Test happy flow of sign and verify'''
        
        message = 'je moeder'
        print("\tMessage:   %r" % message)

        signature = pkcs1.sign(message, self.priv, 'SHA-256')
        print("\tSignature: %r" % signature)

        pkcs1.verify(message, signature, self.pub)

    def test_alter_message(self):
        '''Altering the message should let the verification fail.'''
        
        signature = pkcs1.sign('je moeder', self.priv, 'SHA-256')
        self.assertRaises(pkcs1.VerificationError, pkcs1.verify,
                          'mijn moeder', signature, self.pub)

    def test_sign_different_key(self):
        '''Signing with another key should let the verification fail.'''
        
        (otherpub, _) = rsa.newkeys(512)
        
        message = 'je moeder'
        signature = pkcs1.sign(message, self.priv, 'SHA-256')
        self.assertRaises(pkcs1.VerificationError, pkcs1.verify,
                          message, signature, otherpub)

    def test_multiple_signings(self):
        '''Signing the same message twice should return the same signatures.'''
        
        message = struct.pack('>IIII', 0, 0, 0, 1)
        signature1 = pkcs1.sign(message, self.priv, 'SHA-1')
        signature2 = pkcs1.sign(message, self.priv, 'SHA-1')
        
        self.assertEqual(signature1, signature2)

