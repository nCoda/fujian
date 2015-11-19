#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           fujian
# Program Description:    An HTTP server that executes Python code.
#
# Filename:               setup.py
# Purpose:                Configuration for installation with setuptools.
#
# Copyright (C) 2015 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
'''
Configuration for installation with setuptools.
'''

from setuptools import setup, Command
import fujian  # for __version__


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


_LONG_DESCRIPTION = '''
It’s simple: Fujian accepts Python code in the request body of a PUT request, executes the code, then returns the result.

The server is named after Fujian (福建) Province of the People’s Republic of China. The intention is to use it with our “lychee” software (“litchi” package on PyPI). Lychees are a fruit that grow in southern China. Fujian is a province in southern China. That’s about it.

Do note that this application opens the door to a wide range of security issues, most of which we don’t plan to address. Fujian is intended for use on localhost only. Opening it up to the public Internet is a tremendously bad idea!

We will migrate to PyPy3.
'''


setup(
    name = 'Fujian',
    version = fujian.__version__,
    packages = ['fujian', 'tests'],

    install_requires = ['tornado>=4,<5'],
    tests_require = ['pytest>2.7'],

    cmdclass = {'test': PyTest},

    # metadata for upload to PyPI
    author = 'Christopher Antila',
    author_email = 'christopher@antila.ca',
    description = 'An HTTP server that executes Python code.',
    long_description = _LONG_DESCRIPTION,
    license = 'AGPLv3+',
    keywords = 'tornado, http server, execute python',
    url = 'jameson.adjectivenoun.ca/ncoda/fujian',
)
