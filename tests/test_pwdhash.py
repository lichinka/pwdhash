# -*- coding: utf-8 -*-
import unittest

from pwdhash import PwdHashGenerator



class PwdHashConsoleTest (unittest.TestCase):
    """
    Tests the console interface of the PwdHash generator.-
    """
    def test_ascii_compatibility (self):
        """
        Checks the PwdHash generator is compatible with Standford's version.-
        """
        self.passwd  = "*pepe*"
        self.pwd_gen = PwdHashGenerator (self.passwd)
        self.assertEquals (self.pwd_gen.generate ("google.com"),
                           "uxmCW8+u")

    def test_unicode_compatibility (self):
        """
        Checks that Unicode passwords are accepted and are compatible with
        Standford's version.-
        self.passwd  = "^čufti^"
        self.pwd_gen = PwdHashGenerator (self.passwd)
        self.assertEquals (self.pwd_gen.generate ("google.com"),
                           "+YcFuu8aj")
        """
        pass

