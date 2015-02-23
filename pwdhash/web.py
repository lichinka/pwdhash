# -*- coding: utf-8 -*-
import os
import sys
import cherrypy

from pwdhash.db import KeyDatabase, Key
from pwdhash.platform import copy_to_clipboard



current_dir = os.path.dirname (os.path.abspath (__file__))



class PwdHashServer (object):
    """
    A small server for the PwdHash Vault web interface.-
    """
    #
    # configuration settings for this server
    #
    _global_config = {'server.socket_host' : '127.0.0.1',
                      'server.socket_port' : 8080,
                      'server.thread_pool' : 2}
    #
    # site-specific configuration
    #
    _site_config = {'tools.encode.encoding'  : 'utf-8',
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
        from pwdhash.platform import copy_to_clipboard

        domain = kwargs['domain']
        generated = self.pwd_gen.generate (domain)

        copied_to_clipboard = copy_to_clipboard (generated) 

        if copied_to_clipboard:
            msg = "Password ready"
        else:
            msg = generated
        del generated
        return self.index (msg)

    @cherrypy.expose
    def pick_image (self, query, start=0):
        """
        Displays images from a Google image search, letting the
        user select one as the icon for a new entry:

            query   the query string sent to Google images;
            start   the query parameter for pagination.-
        """
        import json
        import time
        import urllib
        import requests
 
        BASE_URL    = 'https://ajax.googleapis.com/ajax/services/search/images'
        BASE_URL   += '?v=1.0&q=%s' % query
        BASE_URL   += '&start=%d'
        MAX_RESULTS = 56

        img_urls = list ( )

        #
        # display 8 images per page
        #
        start      = int (start)
        next_start = start + 8 
        prev_start = start - 8

        #
        # Google will only return a max of 56 results
        # 
        if next_start > MAX_RESULTS:
            next_start = MAX_RESULTS
        if prev_start < 0:
            prev_start = None
        while start < next_start:
            r = requests.get (BASE_URL % start)
            for image_info in json.loads (r.text)['responseData']['results']:
                url = image_info['unescapedUrl']
                try:
                    image_r = requests.get (url)
                    img_urls.append (url)
                except requests.exceptions.ConnectionError:
                    #
                    # ignore images that are not accessible
                    #
                    pass
            #
            # we get delivered four images per page
            #
            start += 4
             
            # Be nice to Google and they'll be nice back :)
            time.sleep (0.5)
        #
        # disable the link to the next page in case we are at the end
        #
        if next_start == MAX_RESULTS:
            next_start = None
        #
        # render the template
        #
        tmpl = self.jinja_env.get_template ("pick_image.html")
        return tmpl.render (query=urllib.urlencode ({'query': query}),
                            img_urls=img_urls,
                            next_start=next_start,
                            prev_start=prev_start)
     

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



def go (pwd_gen):
    """
    Starts the web-server vault:

    pwd_gen     the PwdHash generator the web app will use.-
    """
    from cherrypy.process.plugins import Daemonizer

    #
    # start the vault as a daemon in the background
    #
    #d = Daemonizer (cherrypy.engine)
    #d.subscribe ( )
   
    print ("Starting PwdHash Vault at %s:%s ..." % (cherrypy.server.socket_host,
                                                    cherrypy.server.socket_port))
    app = PwdHashServer (pwd_gen)
    cherrypy.config.update (PwdHashServer._global_config)
    cherrypy.quickstart    (app,
                            '/',
                            {'/' : PwdHashServer._site_config})

