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

**Plugins**

* :ref:`gwdbvalidator` - Validates automatically all database model requests.

**Patterns**

* :ref:`gwvalidators` - Provides functions to hash and validate python objects.
* :ref:`gwdbvalidators` - Allows the registration of database model classes to validate retrieved data on each
  request.


Why validation is needed
------------------------
Validation is mostly needed, if your application needs input data and must be sure that this data is valid and not
somehow corrupted.

A common case is the usage of files, which must be copied from an external source.
During the transport over the network, the data may get corrupted.
To be sure that this is not the case, a hash of this file can be build and stored beside the file.
After the file is downloaded, the hash is rebuild and compared to the stored one.

Another use case is the usage of databases. If your application is the only one which is allowed to store and change
specific data inside a database, you should be able to validate these data before your plugin is using it again
(This use case is supported by :ref:`gwdbvalidators` and :ref:`gwdbvalidator`).

Who requests validation?
------------------------
In most cases validation may be overengineered, if you are developing a small script for yourself.

However there are scenarios and domains, which need a proven validation of data, so that your application is allowed and
verified to be used inside this domains.

For instance if you are developing solutions for the automotive industry and your solutions may affect the software,
which runs on electronic control units (ECUs) of a car, your application must be
`ISO 26262 <https://en.wikipedia.org/wiki/ISO_26262>`_ compliant. And this normally needs a proven validation
of in- and output data (beside a lot of other stuff).

Installation
------------
Via pip
~~~~~~~
To install ``groundwork-validation`` simply use ``pip``::

   pip install groundwork-validation


From sources
~~~~~~~~~~~~
Using git and pip::

    git clone https://github.com/useblocks/groundwork-validation
    cd groundwork-validation
    pip install -e .


Content
-------

.. toctree::
   :maxdepth: 3

   plugins/index
   patterns/index
   api



