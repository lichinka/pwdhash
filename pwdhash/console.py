import os
import sys
import logging
import subprocess



def console_main (pwd_gen):
    """
    A console interface for PwdHash:

    pwd_gen     the PwdHash generator instance to use.-
    """
    domain    = raw_input ("For domain: ").strip ( )
    generated = pwd_gen.generate (domain)

    #
    # an external program is used for copying the password to the clipboard
    #
    copied_to_clipboard = copy_to_clipboard (generated) 

    if copied_to_clipboard:
        print "Password was copied to clipboard."
    else:
        print generated



def copy_to_clipboard (string):
    """
    Returns 'True' if 'string' was correctly copied to the system's clipboard.-
    """
    #
    # an external program is used for copying the password to the clipboard
    #
    is_copied = False

    if sys.platform == "darwin":
        #
        # on OSX
        #
        clip_copy_exe = "pbcopy"
    elif 'DISPLAY' in os.environ:
        #
        # on Linux/Un*x
        #
        clip_copy_exe = "xclip"

    try:
        pb = subprocess.Popen(clip_copy_exe,
                              stdin=subprocess.PIPE,
                              stdout=open("/dev/null", "w"),
                              stderr=open("/dev/null", "w"))
        pb.communicate (string)
        pb.wait ( )
        if pb.returncode == 0:
            is_copied = True
        else:
            is_copied = False
            logging.warning ("Install '%s' for clipboard support" % clip_copy_exe)
    except:
        is_copied = False

    return is_copied

