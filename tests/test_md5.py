# -*- coding: utf-8 -*-
import unittest

from pwdhash.md5 import HmacMd5



class HmacMd5Test (unittest.TestCase):
    """
    Tests the HMAC-MD5 custom implementation.-
    """
    def test_safe_add (self):
        params   = [[668467704, 2130783302],
                    [-1526234400, -1971324652]]
        expected = [-1495716290,
                      797408244]
        for i in range (len (params)):
            self.assertEqual (HmacMd5._safe_add (*params[i]),
                              expected[i])

    def test_bit_rol (self):
        params   = [  [716240829, 7],
                     [137109738, 12],
                    [-522252520, 17]]
        expected = [ 1484512917,
                    -1039228798,
                      506577342]
        for i in range (len (params)):
            self.assertEqual (HmacMd5._bit_rol (*params[i]),
                            expected[i])


    def test_md5_ff (self):
        params   = [ ]
        expected = [ ]

        params.append ([ 1732584193,
                         -271733879,
                        -1732584194,
                          271733878,
                         1397117766,
                                  7,
                         -680876936])
        expected.append (1212779038)

        params.append ([  271733878,
                         1212779038,
                         -271733879,
                        -1732584194,
                          909522486,
                                 12,
                         -389564586])
        expected.append (173550240)

        params.append ([-1732584194,
                          173550240,
                         1212779038,
                         -271733879,
                          909522486,
                                 17,
                          606105819])
        expected.append (680127582)

        for i in range (len (params)):
            self.assertEqual (HmacMd5._md5_ff (*params[i]),
                              expected[i])


    def test_str2binl (self):
        string   = "pepe"
        expected = [1701864816]
        self.assertEqual (HmacMd5.str2binl (string, 8),
                          expected)

    def test_core_md5 (self):
        chrsz = 8
        lst = [1397117766,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                909522486,
                1735356263,
                1663985004,
                28015]
        expected = [-1906562005,
                     1347505609,
                    -2070658591,
                      639279188]
        result = HmacMd5.core_md5 (lst,
                                   512 + 10 * chrsz)
        self.assertEqual (result,
                          expected)


    def test_core_hmac_md5 (self):
        params   = []
        expected = []

        params.append ([u"^čufti^", "google.com"])
        expected.append ([-1150369439,
                            320447430,
                           2092528897,
                          -2140662759])

        params.append  (["pepe", "google.com"])
        expected.append ([233115305,
                           81019179,
                         -227315827,
                         -927036398])

        for i in range (len (params)):
            self.assertEqual (HmacMd5.core_hmac_md5 (*params[i]),
                              expected[i])

