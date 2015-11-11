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

import fujian


_ACCESS_CONTROL_ALLOW_ORIGIN = 'http://localhost:8000'

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

    def get(self):
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
    exec_this = 'import sys\npost = sys.stdout.get()\ndel sys'
    exec(exec_this, exec_globals, local_locals)
    return local_locals['post']


def get_from_stderr():
    '''
    Get what was written to stderr, with the request's exec_globals, in this request.
    '''
    local_locals = {}
    exec_this = 'import sys\npost = sys.stderr.get()\ndel sys'
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

    def set_default_headers(self):
        '''
        '''
        self.set_header('Server', 'Fujian/{}'.format(fujian.__version__))
        self.set_header('Access-Control-Allow-Origin', _ACCESS_CONTROL_ALLOW_ORIGIN)

    def get(self):
        '''
        Basically this is a ping request.
        '''
        self.write('')

    def post(self):
        '''
        Execute Python code submitted in the request body. Provide the result in the response body,
        either as the output to "stdout" or, if it exists, the value stored in the "fujian_return"
        variable.

        .. note:: The global "fujian_return" variable is set to a zero-length string before any
            code is executed, and deleted just before sending the HTTP response.

        Response Body
        =============

        If the response code is 200, it's a JSON object with three members: stdout, stderr, and
        return. If the response code is 400 (meaning there was an unhandled exception) the object
        also contains a "traceback" member.

        All of these are strings. The "stdout" and "stderr" members are the contents of the
        corresponding stdio streams. The "return" member is the value stored in the global
        "fujian_return" variable at the end of the call. If present, "traceback" contains the
        traceback of the most recent unhandled exception.
        '''
        code = self.request.body
        if not isinstance(code, unicode):
            code = unicode(code)

        # clear stdout, stderr, and fujian_return
        make_new_stdout()
        exec_globals['fujian_return'] = ''

        post = {}

        try:
            exec(code, exec_globals)
        except Exception:
            self.set_status(400)
            post['traceback'] = unicode(get_traceback())

        post['stdout'] = unicode(get_from_stdout())
        post['stderr'] = unicode(get_from_stderr())
        post['return'] = unicode(exec_globals['fujian_return'])
        del exec_globals['fujian_return']

        self.write(post)


if __name__ == "__main__":
    app = web.Application([(r'/', MainHandler),])
    app.listen(1987)
    ioloop.IOLoop.current().start()
