.. _gwfilevalidators:

GwFileValidatorsPattern
=======================

Creating a hash
---------------

For each file a hash value can be created.
:class:`~groundwork_validation.patterns.gw_file_validators_pattern.gw_file_validators_pattern.GwFileValidatorsPattern`
cares about the correct handling of files, even if the file size is too big to get handled in one step.

To create a hash, all you have to do is to use the function
:func:`~groundwork_validation.patterns.gw_file_validators_pattern.gw_file_validators_pattern.FileValidatorsPlugin.hash`::

    from groundwork_validation.patterns import GwFileValidatorsPattern

    class My_Plugin(GwFileValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            my_file = "/path/to/file.txt"

            # Generate and retrieve a string based hash value
            my_hash = self.validators.file.hash(my_file)

            # Store hash value directly into a file
            my_hash = self.validators.file.hash(my_file, hash_file = "/path/to/file.txt.hash")

        def deactivate(self):
            pass

Please see
:func:`~groundwork_validation.patterns.gw_file_validators_pattern.gw_file_validators_pattern.FileValidatorsPlugin.hash`
for a complete list of available parameters.

Validate a file
---------------

Using a hash string
~~~~~~~~~~~~~~~~~~~

For validation the function
:func:`~groundwork_validation.patterns.gw_file_validators_pattern.gw_file_validators_pattern.FileValidatorsPlugin.validate`
is available::

    from groundwork_validation.patterns import GwFileValidatorsPattern

    class My_Plugin(GwFileValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            my_file = "/path/to/file.txt"

            my_hash = self.validators.file.hash(my_file)  # Generate a hash

            if self.validators.file.validate(my_file, my_hash):
                print("Hash is valid")
            else:
                print("Hash is NOT valid")

        def deactivate(self):
            pass

Using a hash file
~~~~~~~~~~~~~~~~~

It is also possible to validate a file against a hash file, which has stored the hash at the first line::

    from groundwork_validation.patterns import GwFileValidatorsPattern

    class My_Plugin(GwFileValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            my_file = "/path/to/file.txt"
            my_hash_file = "/path/to/file.hash"

            if self.validators.file.validate(my_file, hash_file=my_hash_file):
                print("Hash is valid")
            else:
                print("Hash is NOT valid")

        def deactivate(self):
            pass

Please see
:func:`~groundwork_validation.patterns.gw_file_validators_pattern.gw_file_validators_pattern.FileValidatorsPlugin.validate`
for a complete list of available parameters.