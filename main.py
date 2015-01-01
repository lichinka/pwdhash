import sys
import getpass

from pwdhash.generator import PwdHashGenerator



def print_usage ( ):
    """
    Prints out usage message.-
    """
    print ("Usage: %s [-web]" % sys.argv[0])
    print ("Implements Stanford's PwdHash with console and web interfaces.-")
    print
    print ("-web    starts a PwdHash service available through the browser.")


if __name__ == '__main__':
    #
    # ask the user's master password in order to create a generator
    #
    password = getpass.getpass (">>> Please enter your password <<<\n")
    generator = PwdHashGenerator (password)
    del password

    #
    # check command-line parameters
    #
    if len (sys.argv) > 1:
        #
        # start the web server
        #
        if sys.argv[1] == '-web':
            from pwdhash import web
            web.start (generator)
        else:
            print_usage ( )
            sys.exit (1)
    else:
        #
        # start the default console interface
        #
        from pwdhash import console
        console.console_main (generator)

