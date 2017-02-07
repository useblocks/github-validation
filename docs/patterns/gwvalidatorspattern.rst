.. _gwvalidators:

GwValidatorsPattern
===================

This pattern allows plugins to register validators, which can be used to hash and validate python objects.

A validator can be configured to use a specific hash algorithm and hash specific attributes of an given object only.
This maybe necessary, if unhashable python object types are used inside given object.

.. note::
   GwValidatorsPattern uses the `pickle <https://docs.python.org/3.5/library/pickle.html>`_ function of
   Python to build a hashable, binary-based representation of your data.
   There are some data types, which can not be pickeled. In this case the validator must be configured to ignore
   these specific attributes of your data.


Register a new validator
------------------------
To register a new validator, a plugin must inherit from
:class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.GwValidatorsPattern` and use
:func:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.ValidatorsPlugin.register` for
registration::

   from groundwork_validation.patterns import GwValidatorsPattern

    class My_Plugin(GwValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            self.validator = self.validators.register("my_validator", "test validator")



Creating a hash
---------------
Hashes can be build for nearly each python object by using
:func:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.Validator.hash`::

   class My_Plugin(GwValidatorsPattern):
       ...

       def get_hash(self):
            data = "test this"
            self.my_hash = self.validator.hash(data)

Validate an object by given hash
--------------------------------
To validate an object, all you need is the hash and the function
:func:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.Validator.validate`::

    class My_Plugin(GwValidatorsPattern):
        ...

        def validate_hash(self):
            data = "test this"
            if self.validator.validate(data, self.my_hash) is True:
                print("Data is valid")
            else:
                print("Data is invalid. We stop here!")
                sys.exit(1)

.. note::
   The plugin developer is responsible for safely storing hashes (e.g. inside a database).

