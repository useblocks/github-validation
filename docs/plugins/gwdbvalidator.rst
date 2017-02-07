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