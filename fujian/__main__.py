#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           fujian
# Program Description:    An HTTP server that executes Python code.
#
# Filename:               fujian/__main__.py
# Purpose:                This starts everything.
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
This starts everything.
'''

import copy
import sys
import traceback

from tornado import ioloop, web


exec_globals = {'__name__': '__main__', '__builtins__': copy.deepcopy(__builtins__)}


class StdoutHandler(object):
    '''
    This is a replacement for sys.stdout and sys.stderr that collects its output and saves it for
    the stuff.
    '''

    def __init__(self):
        '''
        '''
        self.stuff = ''

    def write(self, write_this):
        '''
        '''
        self.stuff += write_this

    def get_written(self):
        '''
        '''
        return self.stuff


def make_new_stdout():
    '''
    Make a new stdout and stderr, with the request's exec_globals, for a single request.
    '''
    exec_this = 'import sys\nsys.stdout = StdoutHandler()\nsys.stderr = StdoutHandler()\ndel sys'
    exec(exec_this, exec_globals, {'StdoutHandler': StdoutHandler})


def get_from_stdout():
    '''
    Get what was written to stdout, with the request's exec_globals, in this request.
    '''
    local_locals = {}
    exec_this = 'import sys\npost = sys.stdout.get_written()\ndel sys'
    exec(exec_this, exec_globals, local_locals)
    return local_locals['post']


def get_from_stderr():
    '''
    Get what was written to stderr, with the request's exec_globals, in this request.
    '''
    local_locals = {}
    exec_this = 'import sys\npost = sys.stderr.get_written()\ndel sys'
    exec(exec_this, exec_globals, local_locals)
    return local_locals['post']


def myprint(this):
    '''
    Prints "this" using the original stdout, even when it's been replaced. For use in debugging
    ``fujian`` itself.
    '''
    sys.__stdout__.write('{}\n'.format(this))


def get_traceback():
    '''
    Get a traceback of the most recent exception raised in the subinterpreter.
    '''
    typ, val, tb = sys.exc_info()
    err_name = getattr(typ, '__name__', str(typ))
    err_msg = str(val)
    err_trace = traceback.format_exception(typ, val, tb)
    err_trace = ''.join(err_trace)
    # js.globals['pypyjs']._lastErrorName = err_name
    # js.globals['pypyjs']._lastErrorMessage = err_msg
    # js.globals['pypyjs']._lastErrorTrace = err_trace
    return err_trace


class MainHandler(web.RequestHandler):
    '''
    '''

    def get(self):
        '''
        Basically this is a ping request.
        '''
        self.write('')

    def post(self):
        '''
        '''
        code = self.request.body
        if not isinstance(code, unicode):
            code = unicode(code)

        make_new_stdout()

        try:
            exec(code, exec_globals)
        except Exception:
            self.set_status(400)

            post = get_from_stderr()
            if len(post) > 0:
                post += '\n'
            post += get_traceback()

            self.write(post)
        else:
            self.write(get_from_stdout())


if __name__ == "__main__":
    app = web.Application([(r'/', MainHandler),])
    app.listen(1987)
    ioloop.IOLoop.current().start()
