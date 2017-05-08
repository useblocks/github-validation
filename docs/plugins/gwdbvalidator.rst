.. _gwdbvalidator:

GwDbValidator
=============

This plugin automatically activates the validation of all database models, which are
and will be registered via groundwork-database.

On activation ``GwDbValidator`` fetches all existing database models and activates their validation by using
:func:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.DbValidatorsPlugin.register`
of :class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.GwValidatorsPattern`.

It also registers a receiver to get notified, if a new database model is registered.
If this is the case, it also registers a new validator for this new model.

Activation and Usage
--------------------
All you have to do is to activate the plugin, which is done by adding its name to your application configuration::

    LOAD_PLUGINS = ["MyDbPlugin", "MyOtherPlugin", "GwDbValidator"]

That's it. From now on all important database actions get validated.

Configuration
-------------
``GwDbValidator`` is based on
:class:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.DbValidatorsPlugin`
and  therefore needs the same :ref:`gwdbvalidator_config`.

You need to set the parameter **HASH_DB**, which defines the database to be used for storing hash values::

    HASH_DB = "sqlite://%s/hash_db" % APP_PATH


Requirements & Specifications
-----------------------------

The following sections describes the implemented requirements and their related specifications.

**Available requirements**

.. needfilter::
   :tags: gwdbvalidator_plugin
   :types: req
   :layout: table

**Available specifications**

.. needfilter::
   :tags: gwdbvalidator_plugin
   :types: spec
   :layout: table

Requirements
~~~~~~~~~~~~

.. req:: Hashed write requests on database tables
   :tags: gwdbvalidator_plugin;
   :status: implemented
   :id: R_001

   As developer I want my write requests being hashed and available for later use.

.. req:: Validated read requests on database tables
   :tags: gwdbvalidator_plugin;
   :status: implemented
   :id: R_002

   As developer I want to be sure, that all read requests on database tables are validated based on a stored hash

.. req:: Configuration only
   :tags: gwdbvalidator_plugin;
   :status: implemented
   :id: R_003

   As developer I want to activate the validation of all database tables by configuration options only.

Specification
~~~~~~~~~~~~~

.. spec:: Using of groundwork pattern GwDbValidatorPattern
   :tags: gwdbvalidator_plugin;
   :id: S_001
   :status: implemented
   :links: R_001; R_002

   We are using the :ref:`gwdbvalidators` to implement :need:`R_001` und :need:`R_002`.

.. spec:: Automatic database table registration for validation
   :tags: gwdbvalidator_plugin;
   :id: S_002
   :status: implemented
   :links: R_003;

   To easily activate validation of all registered database tables, the plugin needs to perform the following actions
   during activation:

   * Request all already registered database tables and register a new db-validator for them
   * Register a listener for the signal **db_class_registered** and register a new validator every time
     the signal is send and the newly registered database class is provided.

