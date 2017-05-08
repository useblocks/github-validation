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

Requirements & Specifications
-----------------------------

The following sections describes the implemented requirements and their related specifications.

**Available requirements**

.. needfilter::
   :tags: gwvalidator
   :types: req
   :layout: table

**Available specifications**

.. needfilter::
   :tags: gwvalidator
   :types: spec
   :layout: table

Requirements
~~~~~~~~~~~~

.. req:: Validator registration
   :tags: gwvalidator

   As developer I want to register my own specific validator to be able so speccify:

   * name
   * description
   * hash algorithm
   * whitelist for hashable attributes

.. req:: Getting a validator
   :tags: gwvalidator

   As developer I want to get a validator object to use it for handling validations tasks on selected
   objects.

.. req:: Validator functions
   :tags: gwvalidator

   As developer I want my validators to provide the following functions to me:

   * Creating of hashes
   * Validating of hashes

Specification
~~~~~~~~~~~~~

.. spec:: register() function for self.validators
   :tags: gwvalidator
   :links: R_D8C4B; R_6A8AF

   A function ``self.validators.register`` must be implemented, to allow the registration and requesting of validators.

   The register function will have the following parameters:

   * name
   * description
   * algorithm - default is hashlib.sha256
   * whitelist - default is []

   The returned object must be a instance of the class
   :class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.Validator`.

.. spec:: hash() function for validator
   :tags: gwvalidator
   :links: R_E3793;

   An instance of the class
   :class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.Validator`
   has a hash() function, which has the following parameters:

   * data
   * return_hash_object
   * hash_object
   * strict

   Where **data** is the object to hash.

   **hash_object** can be used to provide an hash object, which gets updated instead of creating a new one.

   If **strict** is True, all configured attirbutes from the whitelist must exist inside the given data.

   If **return_hah_object** is True, the hash object, which is used by hashlib will be returned.
   Otherwise a hexdigest string representation.

.. spec:: validate() function for validator
   :tags: gwvalidator
   :links: R_E3793;

   An instance of the class
   :class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.Validator`
   has a validate() function, which has the following parameters:

   * data
   * hash_string

   The **data** is hashed and the calculated hash values is compared against the given **hash_string**.
   If they are equal, True must be returned. Otherwise False.

