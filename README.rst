Fujian
======

.. image:: https://requires.io/github/nCoda/fujian/requirements.svg?branch=master
    :target: https://requires.io/github/nCoda/fujian/requirements/?branch=master
    :alt: Requirements Status
.. image:: https://circleci.com/gh/nCoda/fujian.svg?style=svg
    :target: https://circleci.com/gh/nCoda/fujian
    :alt: Tests on CircleCI
.. image:: https://coveralls.io/repos/nCoda/fujian/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/nCoda/fujian?branch=master
    :alt: Code coverage
.. image:: https://www.quantifiedcode.com/api/v1/project/641802c5628d47be893a607492063514/badge.svg
    :target: https://www.quantifiedcode.com/app/project/641802c5628d47be893a607492063514
    :alt: Code issues
.. image:: https://readthedocs.org/projects/fujian/badge/?version=latest
    :target: https://fujian.readthedocs.org/
    :alt: Project Documentation

PyPI:

.. image:: https://img.shields.io/pypi/v/fujian.svg
    :target: https://pypi.python.org/pypi/fujian
    :alt: Fujian on PyPI
.. image:: https://img.shields.io/pypi/status/fujian.svg
    :alt: Release status
.. image:: https://img.shields.io/pypi/pyversions/fujian.svg
    :alt: Compatible Python versions
.. image:: https://img.shields.io/pypi/implementation/fujian.svg
    :alt: Compatible Python interpreters
.. image:: https://img.shields.io/pypi/l/fujian.svg
    :alt: License


It's simple: Fujian accepts Python code in the request body of a PUT request, executes the code,
then returns the result.

The server is named after Fujian (福建) Province of the Peopl's Republic of China. The intention is
to use it with our "lychee" software ("litchi" package on PyPI). Lychees are a fruit that grow in
southern China. Fujian is a province in southern China. If you're importing lychee (and we do indeed
want to ``import lychee``) they're probably coming from southern China.

Do note that this application opens the door to a wide range of security issues that we don't plan
to address. Fujian is intended for use on ``localhost`` only. Opening it up to the public Internet
is a tremendously bad idea!

Fujian already supports Python 3, and we will add support for PyPy3 when the time comes.
