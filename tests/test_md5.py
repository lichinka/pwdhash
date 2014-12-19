# -*- coding: utf-8 -*-
import unittest

from pwdhash.md5 import HmacMd5



class HmacMd5Test (unittest.TestCase):
    """
    Tests the HMAC-MD5 custom implementation.-
    """
    def test_str2binl (self):
        string   = "pepe"
        expected = [1701864816] 
        
        self.assertEqual (HmacMd5.str2binl (string, 8),
                          expected)


    def test_core_hmac_md5 (self):
        #key  = "^čufti^"
        key  = "pepe"
        data = "google.com"
        expected = [233115305,
                    81019179,
                    -227315827,
                    -927036398]
        
        self.assertEqual (HmacMd5.core_hmac_md5 (key, data),
                          expected)

