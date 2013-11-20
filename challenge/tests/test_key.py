#coding: utf-8

import unittest

from challenge.utils import key


class KeyTestCase(unittest.TestCase):

    def testGenerate(self):
        self.assertEqual(len(key.generate(6)), 6, 'key size')

        for c in key.generate(100):
            self.assertIn(c, ('abcdefghijklmnopqrstuvwxyz'
                              'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                              '0123456789'),
                          'key in range')
