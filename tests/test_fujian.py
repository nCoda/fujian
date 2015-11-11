#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           fujian
# Program Description:    An HTTP server that executes Python code.
#
# Filename:               test/test_fujian.py
# Purpose:                It's got all the tests.
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
It's got all the tests.
'''


from fujian import __main__ as fujian


def test_stdout_handler():
    "It's a test for the StdoutHandler class."

    handler = fujian.StdoutHandler()
    assert '' == handler.get()
    handler.write('what what')
    assert 'what what' == handler.get()
    handler.write(' in the (censored)')
    assert 'what what in the (censored)' == handler.get()
