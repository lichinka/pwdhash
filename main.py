# -*- coding: utf-8 -*-
import sys



def create_generator ( ):
    """
    Returns an instantiated PwdHashGenerator object with the
    user's master password.-
    """
    import getpass
    from pwdhash.generator import PwdHashGenerator

    #
    # ask the user's master password in order to create a generator
    #
    password = unicode (getpass.getpass (">>> Please enter your password <<<\n"),
                        'utf8')
    generator = PwdHashGenerator (password)
    del password
    return generator


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

            generator = create_generator ( )
            console.go (generator)
        else:
            print_usage ( )
            sys.exit (1)
    else:
        #
        # start the web interface in a separate process
        #
        from multiprocessing import Process
        from pwdhash.web import go, PwdHashServer
        from pwdhash.platform import open_target
        
        generator = create_generator ( )
        p = Process (target=go, args=(generator,))
        p.start ( )

        #
        # display the Vault's home page in a browser
        #
        vault_home = 'http://%s:%s' % (PwdHashServer._global_config['server.socket_host'],
                                       PwdHashServer._global_config['server.socket_port'])
        open_target (vault_home)
        
        #
        # the Vault's process
        #
        p.join ( )



if __name__ == '__main__':
    main ( )
