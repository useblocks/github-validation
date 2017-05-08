.. _gwcmdvalidators:

GwCmdValidatorsPattern
======================
The
:class:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.GwCmdValidatorsPattern`
can be used to valid the execution of a command.

This can helpful to verify the version of an installed tool by checking, if the output
contains the correct version.

For some cases also the correct behavior can be validated by checking the correct return value or by setting a limit
for the maximum allowed execution time.

Validating the output of a command
----------------------------------

All different types of command validations are available by using the function
:func:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.CmdValidatorsPlugin.validate`:

.. code-block:: python

      import sys
      from groundwork_validation.patterns import GwCmdValidatorsPattern

      class My_Plugin(GwCmdValidatorsPattern):
            def __init__(self, app, **kwargs):
                self.name = "My_Plugin"
                super(My_Plugin, self).__init__(app, **kwargs)

            def activate(self):
                if self.validators.cmd.validate("dir", search="my_folder"):
                    print("Command 'dir' works as expected.")
                else:
                    print("Command 'dir' seems not to work correctly. We stop here")
                    sys.exit(1)

            def deactivate(self):
                pass

Instead of searching for a specific string, you can also use a regular expression::

    # Checks for an e-mail address
    if self.validators.cmd.validate("dir",
                                    regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"):
        print("Found at least one e-mail address")



Validating the return code
--------------------------

By validating the return code, you can easily check if the command is available and exits like expected.
If the return code is not allowed, the exception
:class:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.NotAllowedReturnCode`
is raised:

.. code-block:: python

    import sys
    from groundwork_validation.patterns import GwCmdValidatorsPattern
    from groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern import NotAllowedReturnCode

     class My_Plugin(GwCmdValidatorsPattern):
            def __init__(self, app, **kwargs):
                self.name = "My_Plugin"
                super(My_Plugin, self).__init__(app, **kwargs)

            def activate(self):
                try:
                    if self.validators.cmd.validate("dir", search="my_folder", allowed_return_codes=[0, 1]):
                        print("Command 'dir' works a expected.")
                    else:
                        print("Command 'dir' seems not to work correctly. We stop here")
                        sys.exit(1)
                except NotAllowedReturnCode:
                    print("Command exists with not allowed status code. Validation failed!")
                    sys.exit(1)




Setting a timeout
-----------------

By default the command is killed after a timeout of 2 seconds and
:class:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.CommandTimeoutExpired`
is raised. You are free to set your own timeout for each validation::

    import sys
    from groundwork_validation.patterns import GwCmdValidatorsPattern
    from groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern \
        import NotAllowedReturnCode, CommandTimeoutExpired

    class My_Plugin(GwCmdValidatorsPattern):
            def __init__(self, app, **kwargs):
                self.name = "My_Plugin"
                super(My_Plugin, self).__init__(app, **kwargs)

            def activate(self):
                try:
                    if self.validators.cmd.validate("dir", search="my_folder", timeout=5):
                        print("Command 'dir' works a expected.")
                    else:
                        print("Command 'dir' seems not to work correctly. We stop here")
                        sys.exit(1)
                except CommandTimeoutExpired:
                    print("Command has not finished and raised a timeout. This is not expected. We stop here!")
                    sys.exit(1)


test::

    pip install

Requirements & Specifications
-----------------------------

The following sections describes the implemented requirements and their related specifications.

**Available requirements**

.. needfilter::
   :tags: gwcmdvalidators
   :types: req
   :layout: table

**Available specifications**

.. needfilter::
   :tags: gwcmdvalidators
   :types: spec
   :layout: table

Requirements
~~~~~~~~~~~~

.. req:: Command output validation
   :tags: gwcmdvalidators

   As developer I want to be able to validate the correct output of an executed command.

.. req:: Command exit code validation
   :tags: gwcmdvalidators

   As developer I want to be able to validate the correct exit code of an executed command

.. req:: Command runtime validation
   :tags: gwcmdvalidators

   As developer I want to be able to validate the maximum needed run time of an executed command

Specifications
~~~~~~~~~~~~~~

.. spec:: Command execution
   :tags: gwcmdvalidators
   :links: R_79027;R_72AC6;R_77A07

   With `self.validators.cmd.validate` the developer is able to execute a command on command line.
   This execution takes place in a subprocess, but the application must wait till it ends.

   The first argument must be the command to execute

.. spec:: command output check
   :tags: gwcmdvalidators
   :links: R_79027

   As keyword argument "search" of `self.validators.cmd.validate` the output on STDOUT is checked, if the
   given string is part of it.

   If yes, True is returned. Otherwise False

.. spec:: command exit code check
   :tags: gwcmdvalidators
   :links: R_72AC6

   As keyword argument "allowed_return_codes" of `self.validators.cmd.validate` as list of allowed return
   codes can be defined.

   If the retrieved return code is not in this list, the Error
   :class:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.NotAllowedReturnCode`
   is raised.

.. spec:: command timeout check
   :tags: gwcmdvalidators
   :links: R_77A07

   As keyword argument "timeout" of `self.validators.cmd.validate` a time in seconds can be set.

   If the execution of the given command takes longer as specified, the execution is aborted and the error
   :class:`~groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern.CommandTimeoutExpired`
   is raised.
