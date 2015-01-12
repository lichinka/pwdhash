# -*- coding: utf-8 -*-
import sys
import getpass

from pwdhash.generator import PwdHashGenerator



def print_usage ( ):
    """
    Prints out usage message.-
    """
    print ("Usage: %s [-i]" % sys.argv[0])
    print ("Implements Stanford's PwdHash with console and web interfaces.")
    print
    print ("-i    starts PwdHash in interactive mode.-")


def main ( ):
    """
    PwdHash entry point.-
    """
    #
    # check command-line parameters
    #
    start_obj = None

    if len (sys.argv) > 1:
        #
        # console interface?
        #
        if sys.argv[1] == '-i':
            from pwdhash import console
            start_obj = console
        else:
            print_usage ( )
            sys.exit (1)
    else:
        #
        # start the web interface by default
        #
        from pwdhash import web
        start_obj = web
    #
    # ask the user's master password in order to create a generator
    #
    password = unicode (getpass.getpass (">>> Please enter your password <<<\n"),
                        'utf8')
    generator = PwdHashGenerator (password)
    del password
    #
    # start the selected interface
    #
    start_obj.go (generator)



if __name__ == '__main__':
    main ( )
