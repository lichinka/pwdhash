# -*- coding: utf-8 -*-
import os
import sys
import cherrypy

from pwdhash.db import KeyDatabase, Key
from pwdhash.console import copy_to_clipboard



current_dir = os.path.dirname (os.path.abspath (__file__))



class PwdHashServer (object):
    """
    A small web server for the PwdHash web interface.-
    """
    def _get_config (self):
        """
        Returns the configuration dictionary for this webb app.-
        """
        #
        # start the server with only two threads
        #
        cherrypy.config.update ({'server.thread_pool': 2})
        #
        # site-specific configuration
        #
        return {'tools.encode.encoding'  : 'utf-8',
                'tools.secureheaders.on' : True,
                'tools.staticdir.on'     : True,
                'tools.staticdir.dir'    : '%s/%s' % (current_dir, "static")}


    def _secure_headers (self):
        """
        These settings provide enhanced security to the served pages.-
        """
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Content-Security-Policy'] = "default-src='self'"


    def __init__ (self, pwd_gen):
        """
        Creates a new web application object:

        pwd_gen     the PwdHash generator instance this web app uses.-
        """
        from jinja2 import Environment, PackageLoader

        self.pwd_gen = pwd_gen
        #
        # template-rendering environment
        #
        self.jinja_env = Environment (loader=PackageLoader ('pwdhash',
                                                            'templates'))
        #
        # set the security settings on the 'before_finalize' hook point
        #
        cherrypy.tools.secureheaders = cherrypy.Tool ('before_finalize',
                                                      self._secure_headers,
                                                      priority=60)
        #
        # turn off logging to standard output
        #
        cherrypy.log.screen = None
       
        #
        # initialize the database
        #
        self.db = KeyDatabase (current_dir)


    @cherrypy.expose
    def about (self):
        """
        The 'about' page.-
        """
        tmpl = self.jinja_env.get_template ("about.html")
        return tmpl.render ( )


    @cherrypy.expose
    def add (self):
        """
        This page allows to save a new key.-
        """
        tmpl = self.jinja_env.get_template ("add.html")
        return tmpl.render ( )


    @cherrypy.expose
    def generate (self, *args, **kwargs):
        """
        This target generates a PwdHash password.-
        """
        import subprocess

        domain = kwargs['domain']
        generated = self.pwd_gen.generate (domain)

        #
        # an external program is used for copying the password to the clipboard
        #
        copied_to_clipboard = copy_to_clipboard (generated) 

        if copied_to_clipboard:
            msg = "Password ready"
        else:
            msg = generated
        raise cherrypy.HTTPRedirect ("/?msg=%s" % msg)


    @cherrypy.expose
    def index (self, msg=None):
        """
        The 'index' page.-
        """
        #
        # clean the clipboard if there is no 'msg'
        #
        if msg is None:
            copy_to_clipboard ("***")
        #
        # get a list of all the available keys
        #
        keys = Key.select ( ).orderBy ('name')
        #
        # render the template
        #
        tmpl = self.jinja_env.get_template ("index.html")
        return tmpl.render (keys=keys,
                            msg=msg)


    @cherrypy.expose
    def update (self, name=None, domain=None, image=None, delete=None):
        """
        Updates a key in the vault.-
        """
        from sqlobject import SQLObjectNotFound

        #
        # delete an entry?
        #
        if delete:
            try:
                k = Key.byName (delete)
                Key.delete (k.id)
            except SQLObjectNotFound:
                pass
        #
        # add or update an entry?
        #
        elif name:
            #
            # if the entry already exists, we will update it
            #
            try:
                k = Key.byName (name)
            except SQLObjectNotFound:
                k = Key (name=name,
                         domain=domain,
                         image=image)
            #
            # update the rest of the fields
            #
            k.domain = domain
            k.image  = image
        #
        # go back home
        #
        raise cherrypy.HTTPRedirect ("/")



def start_server (pwd_gen):
    """
    Starts the web server and opens the browser on the index page:

    pwd_gen     the PwdHash generator the web app will use.-
    """
    print ("Starting PwdHash server at %s:%s ..." % (cherrypy.server.socket_host,
                                                     cherrypy.server.socket_port))
    app = PwdHashServer (pwd_gen)
    cherrypy.quickstart (app,
                         '/',
                         {'/' : app._get_config ( )})

