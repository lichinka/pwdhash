import os
import sys
import logging
import subprocess



def open_target (tgt):
    """
    Opens 'tgt' using the system-registered application.-
    """
    if sys.platform == "darwin":
        #
        # on OSX
        #
        open_exe = "open"
    elif 'DISPLAY'in os.environ:
        #
        # on Linux/Un*x
        #
        open_exe = "xdg-open"
    try:
        pb = subprocess.Popen ([open_exe, tgt],
                               stdout=open("/dev/null", "w"),
                               stderr=open("/dev/null", "w"))
        pb.wait ( )
    except OSError:
        logging.warning ("Could not open [%s]" % tgt)
    else:
        if pb.returncode != 0:
            logging.warning ("Could not open [%s]" % tgt)
 
    

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

