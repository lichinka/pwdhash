# -*- coding: utf-8 -*-
import os
import apsw

from sqlobject import *



class KeyDatabase (object):
    """
    Keeps track of the registered keys inside a PwdHash vault.-
    """
    def __init__ (self, cur_dir):
        """
        Initializes the database, using 'cur_dir' as the base directory.-
        """
        db_path     = os.path.abspath ('%s/data.db' % cur_dir)
        conn_string = 'sqlite:%s' % db_path
        connection  = connectionForURI (conn_string)
        sqlhub.processConnection = connection

        #
        # create the database if it doesn't exist
        #
        Key.createTable (ifNotExists=True)
        Key._connection.debug = False



class Key (SQLObject):
    """
    A key inside the PwdHash vault.-
    """
    #
    # using alternateID will automatically create a byName() method
    #
    name   = StringCol (alternateID=True, unique=True)
    domain = StringCol ( )
    image  = StringCol ( )

