import os
import sys
import logging
import subprocess



def go (pwd_gen):
    """
    A console interface for PwdHash:

    pwd_gen     the PwdHash generator instance to use.-
    """
    from pwdhash.platform import copy_to_clipboard

    domain    = raw_input ("For domain: ").strip ( )
    generated = pwd_gen.generate (domain)

    #
    # an external program is used for copying the password to the clipboard
    #
    copied_to_clipboard = copy_to_clipboard (generated) 

    if copied_to_clipboard:
        print ("Password copied to clipboard.")
    else:
        print (generated)
