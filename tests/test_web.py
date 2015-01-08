import cherrypy
from cherrypy.test import helper

from pwdhash.web import PwdHashServer
from pwdhash.generator import PwdHashGenerator



class PwdHashServerTest (helper.CPWebCase):
    """
    Tests the web interface of the PwdHash generator.-
    """
    def setup_server ( ):
        #
        # instantiate the password generator used by the web app
        #
        passwd = "pepe"
        pwd_gen = PwdHashGenerator (passwd)
        #
        # start the web-app server
        #
        cherrypy.tree.mount (PwdHashServer (pwd_gen))
    #
    # this method creates the testing environment
    #
    setup_server = staticmethod (setup_server)


    def test_index (self):
        """
        Checks the index page is correctly served.-
        """
        self.getPage ('/')
        self.assertStatus ('200 OK')
        self.assertHeader ('Content-Type', 'text/html;charset=utf-8')
        self.assertInBody ('PwdHash Vault')
        self.assertInBody ('ABOUT')


    def test_about (self):
        """
        Checks the 'About' page is correctly served.-
        """
        self.getPage ('/about')
        self.assertStatus ('200 OK')
        self.assertHeader ('Content-Type', 'text/html;charset=utf-8')
        self.assertInBody ('theft-resistant')
        self.assertInBody ('HOME')


    def test_add (self):
        """
        Checks the 'Add' page is correctly served.-
        """
        self.getPage ('/add')
        self.assertStatus ('200 OK')
        self.assertHeader ('Content-Type', 'text/html;charset=utf-8')
        self.assertInBody ('Site Address')
        self.assertInBody ('Add key')

