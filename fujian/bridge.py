#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           fujian
# Program Description:    An HTTP server that executes Python code.
#
# Filename:               fujian/bridge.py
# Purpose:                This module is a bridge from Fujian to Lychee.
#
# Copyright (C) 2017 Christopher Antila
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
This module is a bridge from Fujian to Lychee.
'''

import json

import fujian
import lychee


def process_signal(ws_handler, signal, session, tempdirs):
    '''
    Do whatever is required for a signal incoming via WebSocket.

    :param str signal: The encoded signal data (currently JSON object).
    :param session: The :class:`InteractiveSession` to use.
    :param dict tempdirs: The dictionary of temporary directories.
    '''
    signal = json.loads(signal)

    if signal['type'] == 'lilypond_pdf':
        try:
            session.registrar.register('lilypond', 'Fujian bridge')
            def the_outputter(**kwargs):
                '''Callback for CONVERSION_FINISHED.'''
                if kwargs['dtype'] == 'lilypond':
                    pdf_path = fujian.lilypond.render_lilypond_pdf(kwargs['document'], tempdirs)
                    ws_handler.write_message(json.dumps({
                        'type': 'lilypond_pdf',
                        'payload': pdf_path,
                        'meta': signal['payload'],
                    }))

            lychee.signals.outbound.CONVERSION_FINISHED.connect(the_outputter)
            session.run_outbound(views_info=signal['payload'])  # TODO: choose section dynamically

        finally:
            session.registrar.unregister('lilypond', 'Fujian bridge')
            lychee.signals.outbound.CONVERSION_FINISHED.disconnect(the_outputter)
