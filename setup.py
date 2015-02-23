#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import subprocess
from setuptools import setup, find_packages



version = '0.0.1'


def read (fname):
    """
    Returns the content of 'fname' as a string.-
    """
    return open (os.path.join (os.path.dirname (__file__), fname)).read ( )


def check_for_sqlite ( ):
    """
    Checks the availability of ``sqlite`` in the target system
    and returns its version or None if it was not found.-
    """
    prg = 'sqlite3'
    ret_value = None

    try:
        pb = subprocess.Popen ([prg, '--version'],
                               stdout=subprocess.PIPE,
                               stderr=open("/dev/null", "w"))
        out, err = pb.communicate ( )
    except OSError:
        logging.error ("Please install '%s' or add it to your path" % prg)
        ret_value = None
    else:
        if pb.returncode != 0:
            logging.error ("Please install '%s' or add it to your path" % prg)
            ret_value = None
        else:
            ret_value = out.split (' ')[0]
    return ret_value


def get_requirements (fname):
    """
    Gets a list of requirements from the content of 'fname'.-
    """
    req = read ('requirements.txt') % check_for_sqlite ( )
    return req.split ('\n')



setup (name='pwdhash-vault',
       version=version,
       description="A local password vault using Stanford's PwdHash",
       long_description=read ('README.md'),
       classifiers=['Development Status :: 5 - Production/Stable',
                    'Environment :: Console',
                    'Environment :: Web Environment',
                    'Environment :: X11 Applications',
                    'Environment :: MacOS X',
                    'License :: OSI Approved :: BSD License',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Internet',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Utilities',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',],
       keywords='local pwdhash vault',
       author='Lucas Benedicic',
       author_email='lucas.benedicic@gmail.com',
       url='https://github.com/lichinka/pwdhash-vault',
       license='BSD',
       py_modules=['main'],
       packages=['pwdhash'],
       include_package_data=True,
       install_requires=get_requirements ('requirements.txt'),
       entry_points={ 'console_scripts': [ 'pwdhash = main:main' ] },
       zip_safe=False,
      )
      
