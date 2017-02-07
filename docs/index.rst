.. image:: https://img.shields.io/pypi/l/groundwork-validation.svg
   :target: https://pypi.python.org/pypi/groundwork-validation
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/groundwork-validation.svg
   :target: https://pypi.python.org/pypi/groundwork-validation
   :alt: Supported versions
.. image:: https://readthedocs.org/projects/groundwork-validation/badge/?version=latest
   :target: https://readthedocs.org/projects/groundwork-validation/
.. image:: https://travis-ci.org/useblocks/groundwork-validation.svg?branch=master
   :target: https://travis-ci.org/useblocks/groundwork-validation
   :alt: Travis-CI Build Status
.. image:: https://coveralls.io/repos/github/useblocks/groundwork-validation/badge.svg?branch=master
   :target: https://coveralls.io/github/useblocks/groundwork-validation?branch=master
.. image:: https://img.shields.io/scrutinizer/g/useblocks/groundwork-validation.svg
   :target: https://scrutinizer-ci.com/g/useblocks/groundwork-validation/
   :alt: Code quality
.. image:: https://img.shields.io/pypi/v/groundwork-validation.svg
   :target: https://pypi.python.org/pypi/groundwork-validation
   :alt: PyPI Package latest release

Welcome to groundwork validation
================================

.. _groundwork: https://groundwork.readthedocs.io

.. sidebar:: groundwork framework

   `groundwork`_ is a plugin based Python application framework, which can be used to create various types of applications:
   console scripts, desktop apps, dynamic websites and more.

   Visit `groundwork.useblocks.com <http://groundwork.useblocks.com>`_
   or read the `technical documentation <https://groundwork.readthedocs.io>`_ for more information.

This Python package is designed for applications, which are based on the
`groundwork application framework <https://groundwork.readthedocs.io>`_.

All of its plugins and patterns are focused on application validation during runtime.

This package contains the following groundwork extensions:

 * Plugins

  * **GwDbValidator** - Validates automatically each database model request

 * Patterns

   * **GwValidatorsPattern** - Provides functions to hash and valid python objects.
   * **GwDbValidatorsPattern** - Allows the registration of specific database model classes, so that their requests get validated.

Installation
------------

To install ``groundwork-validation`` simply use ``pip``::

   pip install groundwork-validation

Content
-------

.. toctree::
   :maxdepth: 2

   patterns/index
   plugins/index

