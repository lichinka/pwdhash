import os, sys, subprocess



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
    copied_to_clipboard = False

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
        pb.communicate(generated)
        pb.wait()
        if pb.returncode == 0:
            copied_to_clipboard = True
        else:
            sys.stderr.write ("Install '%s' for clipboard support\n" % clip_copy_exe)
    except:
        pass

    if copied_to_clipboard:
        print "Password was copied to clipboard."
    else:
        print generated

