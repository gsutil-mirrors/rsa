'''Tests string operations.'''

import struct
import unittest

import rsa
from rsa.common import gcd

class KeyGenTest(unittest.TestCase):

    def test_exp_coef(self):
        '''Tests the exp1, exp2 and coef values.'''

        (_, priv) = rsa.newkeys(256)

        self.assertEqual(gcd(priv.exp1, priv.p - 1), 1)
        self.assertEqual(gcd(priv.exp2, priv.q - 1), 1)

        self.assertEqual(priv.d    % (priv.p - 1),
                         priv.exp1 % (priv.p - 1))

        self.assertEqual(priv.d    % (priv.q - 1),
                         priv.exp2 % (priv.q - 1))


        self.assertEqual(priv.exp1 % 2, priv.exp2 % 2)

        
