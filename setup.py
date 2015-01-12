#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from setuptools import setup, find_packages



version = '0.2.0'


def read (fname):
    """
    Utility function to read the README file; used for the long_description.-
    """
    return open (os.path.join (os.path.dirname (__file__), fname)).read ( )


setup (name='pwdhash',
       version=version,
       description="An implementation of Stanford's PwdHash",
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
       author='Lev Shamardin, Lucas Benedicic',
       author_email='shamardin@gmail.com, lucas.benedicic@gmail.com',
       url='https://github.com/abbot/pwdhash',
       license='BSD',
       py_modules=['main'],
       packages=['pwdhash'],
       include_package_data=True,
       install_requires=['CherryPy', 'Jinja2', 'SQLObject', 'apsw', 'nose'],
       entry_points={ 'console_scripts': [ 'pwdhash = main:main' ] },
       zip_safe=False,
      )
      
