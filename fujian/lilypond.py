#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           fujian
# Program Description:    An HTTP server that executes Python code.
#
# Filename:               fujian/lilypond.py
# Purpose:                Handles LilyPond interaction on behalf of Fujian.
#
# Copyright (C) 2017 Jeff Treviño, Christopher Antila
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
Handles LilyPond interaction on behalf of Fujian.
'''

import datetime
import os
import subprocess
import sys

_LY_DEFAULT_ON_LINUX = '/usr/bin/lilypond'
_LY_DEFAULT_ON_MACOS = '/Applications/LilyPond.app/Contents/Resources/bin/lilypond'
_LY_DEFAULT_ON_WINDOWS = 'C:\\Program Files (x86)\\LilyPond\\Resources\\usr\\bin\\lilypond.exe'


def find_lilypond():
    '''
    Find the executable LilyPond binary.

    :returns: The executable path.
    :rtype: string
    :raises: :exc:`RuntimeError` if LilyPond cannot be found.
    '''
    post = None

    if os.name == 'posix':
        if subprocess.call(['which', 'lilypond']) == 0:
            post = 'lilypond'
        elif sys.platform == 'linux2' and os.path.isfile(_LY_DEFAULT_ON_LINUX):
            post = _LY_DEFAULT_ON_LINUX
        elif sys.platform == 'darwin' and os.path.isfile(_LY_DEFAULT_ON_MACOS):
            post = _LY_DEFAULT_ON_MACOS

    elif os.name == 'nt':
        if subprocess.call(['where', 'lilypond']) == 0:
            post = 'lilypond'
        elif os.path.isfile(_LY_DEFAULT_ON_WINDOWS):
            post = _LY_DEFAULT_ON_WINDOWS

    if post:
        return post
    else:
        raise RuntimeError('Cannot find LilyPond.')


def render_lilypond_pdf(ly_string, tempdirs):
    '''
    Use LilyPond to render a PDF.

    :param str ly_string: The LilyPond document to render.
    :param dict tempdirs: The :const:`TEMPDIRS` object for this *Fujian* instance.
    :returns: The absolute path to the rendered PDF document.
    :rtype: str
    '''
    command = find_lilypond()

    tempdir = tempdirs['lily-to-pdf']
    raw_filename = datetime.datetime.now().strftime('%H%M%S%f')
    ly_filename = os.path.join(tempdir, '{0}.ly'.format(raw_filename))
    pdf_filename = os.path.join(tempdir, '{0}.pdf'.format(raw_filename))

    with open(ly_filename, 'w') as lily_file:
        lily_file.write(ly_string)

    subprocess.call([command, '-o', tempdir, ly_filename])

    return pdf_filename
