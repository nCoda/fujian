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
# import lychee
from abjad import lilypondfiletools


_RENDER_LILYPOND_PDF = False


def get_show_abjad(session):
    '''
    Returns the show_abjad() function.
    '''
    def show_abjad(abj_obj):
        '''
        A Fujian-specific replacement for Abjad's show() method that connects to Lychee.
        '''
        lilypondfile = lilypondfiletools.make_basic_lilypond_file(abj_obj)
        session.run_workflow(dtype='lilypond', doc=format(lilypondfile))

    return show_abjad


def process_signal(ws_handler, signal, session, tempdirs):
    '''
    Do whatever is required for a signal incoming via WebSocket.

    :param str signal: The encoded signal data (currently JSON object).
    :param session: The :class:`InteractiveSession` to use.
    :param dict tempdirs: The dictionary of temporary directories.
    '''
    global _RENDER_LILYPOND_PDF
    signal = json.loads(signal)

    if signal['type'] == 'lilypond_pdf':
        try:
            _RENDER_LILYPOND_PDF = True
            session.registrar.register('lilypond', 'Fujian bridge')
            session.run_outbound(views_info=signal['payload'])
        finally:
            _RENDER_LILYPOND_PDF = False
            session.registrar.unregister('lilypond', 'Fujian bridge')

    elif signal['type'] == 'fujian.REGISTER_OUTBOUND_FORMAT':
        session.registrar.register(
            signal['payload']['dtype'],
            signal['payload']['who'],
            signal['payload']['runNow'],
        )

    elif signal['type'] == 'fujian.UNREGISTER_OUTBOUND_FORMAT':
        session.registrar.unregister(
            signal['payload']['dtype'],
            signal['payload']['who'],
        )

    else:
        raise RuntimeError('Fujian received an unknown signal from Julius')


def conversion_finished(instance, dtype, document, placement, **kwargs):
    '''
    Converts the Lychee "outbound.CONVERSION_FINISHED" signal to a Redux action for Julius.
    '''
    if dtype == 'document':
        serialized_sections = json.dumps(
            document.get('sections', {}),
            separators=(',', ':'),
            sort_keys=True,
        )

        # Only dispatch this action if the sections have changed.
        # If we dispatch UPDATED_SECTIONS when the sections were not changed, then most of the
        # stores will empty themselves and we lose all the Redux state.
        if instance._sections != serialized_sections:
            first_redux_action = {
                'is_fsa': True,
                'type': 'document.types.WILL_UPDATE_SECTIONS',
                'meta': {
                    'dtype': dtype,
                    'placement': placement,
                },
                'payload': document.get('sections', {}),
            }
            instance.write_message(json.dumps(first_redux_action))

            second_redux_action = {'is_fsa': True, 'type': 'document.types.UPDATED_SECTIONS'}
            instance.write_message(json.dumps(second_redux_action))

            instance._sections = serialized_sections


    else:
        redux_action = {
            'is_fsa': True,
            'type': 'document.types.UPDATE_SECTION_DATA',
            'meta': {
                'dtype': dtype,
                'placement': placement,
            },
            'payload': document,
        }
        instance.write_message(json.dumps(redux_action))

        if dtype == 'lilypond' and _RENDER_LILYPOND_PDF:
            pdf_path = fujian.lilypond.render_lilypond_pdf(kwargs['document'], tempdirs)
            redux_action = {
                'is_fsa': True,
                'type': 'lilypond.types.UPDATE_PDF',
                'payload': pdf_path,
                'meta': placement,
            }
            instance.write_message(json.dumps(redux_action))


def conversion_errored(instance, msg=None, **kwargs):
    '''
    Converts the "outbound.ERROR" signal to a Redux action for Julius.
    '''
    if msg:
        message = 'Error during outbound conversion: {0}'.format(msg)
    else:
        message = 'Error during outbound conversion.'

    instance.write_message(json.dumps({
        'is_fsa': True,
        'type': 'meta.types.WRITE_STDIO',
        'payload': message,
    }))


def log_message(instance, level=None, logger=None, message=None, status=None, time=None, **kwargs):
    '''
    Converts the "LOG_MESSAGE" signal for use by Julius (not a Redux action).
    '''
    pass


SIGNAL_TO_HANDLER = {
    'LOG_MESSAGE': log_message,
    'outbound.CONVERSION_FINISHED': conversion_finished,
    'outbound.ERROR': conversion_errored,
}
