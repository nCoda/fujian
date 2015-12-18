Fujian
======

.. image:: https://requires.io/github/nCoda/fujian/requirements.svg?branch=master
     :target: https://requires.io/github/nCoda/fujian/requirements/?branch=master
     :alt: Requirements Status
.. image:: https://travis-ci.org/nCoda/fujian.svg?branch=master
    :target: https://travis-ci.org/nCoda/fujian
.. image:: https://coveralls.io/repos/nCoda/fujian/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/nCoda/fujian?branch=master
.. image:: https://readthedocs.org/projects/fujian/badge/?version=latest
    :target: https://fujian.readthedocs.org/

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
