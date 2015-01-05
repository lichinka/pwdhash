# -*- coding: utf-8 -*-
import os
import sys
import cherrypy



current_dir = os.path.dirname (os.path.abspath (__file__))



class PwdHashServer (object):
    """
    A small web server for the PwdHash web interface.-
    """
    def _get_config (self):
        """
        Returns the comnfiguration dictionary for this webb app.-
        """
        return {'tools.secureheaders.on' : True,
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


    @cherrypy.expose
    def index (self):
        """
        The 'index.html' page.-
        """
        index_template = self.jinja_env.get_template ("index.html")

        return index_template.render ( )


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
                return ("Install '%s' for clipboard support\n" % clip_copy_exe)
        except:
            pass

        if copied_to_clipboard:
            return "<h2>Password copied to clipboard</h2>"
        else:
            return generated





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

