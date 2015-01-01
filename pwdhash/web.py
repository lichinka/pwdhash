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
        return {'tools.staticdir.on'  : True,
                'tools.staticdir.dir' : '%s/%s' % (current_dir, "static")}


    def __init__ (self, pwd_gen):
        """
        Creates a new web application object:

        pwd_gen     the PwdHash generator instance this web app uses.-
        """
        self.pwd_gen = pwd_gen


    @cherrypy.expose
    def index (self):
        """
        The 'index.html' page.-
        from jinja2 import Environment, PackageLoader

        #
        # initialize the template renderer environment
        #
        jinja_env = Environment (loader=PackageLoader (current_dir,
                                                       'templates'))
        index_template = jinja_env.get_template ("index.html")

        return index_template.render ( )
        """
        return 'ok!'


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





def start (pwd_gen):
    """
    Start the web server and opens the browser on its index page:

    pwd_gen     the PwdHash generator the web app will use.-
    """
    app = PwdHashServer (pwd_gen)
    cherrypy.quickstart (app,
                         '/',
                         {'/' : app._get_config ( )})

