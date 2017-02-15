import os
import pytest
import groundwork
from groundwork_validation.patterns import GwCmdValidatorsPattern
from groundwork_validation.patterns.gw_cmd_validators_pattern.gw_cmd_validators_pattern \
    import NotAllowedReturnCode, CommandTimeoutExpired


def test_cmd_validator_init():
    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()


def test_cmd_validator_search(tmpdir):
    # Creating temporay folder with sub_folders
    tmpdir.mkdir("sub_a")
    tmpdir.mkdir("sub_b")
    tmpdir.mkdir("sub_c")

    # Change working directory to temporary folder
    old_cwd = os.getcwd()
    os.chdir(str(tmpdir))

    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()

    assert plugin.validators.cmd.validate("dir", search="sub_a") is True
    assert plugin.validators.cmd.validate("dir", search="NO_KNOWN_FOLDER") is False

    # Let's change back the working dir, maybe this isn't done pytest itself after each test
    os.chdir(old_cwd)


def test_cmd_validator_regex(tmpdir):

    # Creating temporay folder with sub_folders
    tmpdir.mkdir("sub_a")
    tmpdir.mkdir("sub_b")
    tmpdir.mkdir("sub_c")

    # Change working directory to temporary folder
    old_cwd = os.getcwd()
    os.chdir(str(tmpdir))

    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()

    assert plugin.validators.cmd.validate("dir", regex="sub*") is True
    assert plugin.validators.cmd.validate("dir", regex="sub_NO*") is False

    # Let's change back the working dir, maybe this isn't done pytest itself after each test
    os.chdir(old_cwd)


def test_cmd_validator_return_codes():
    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()

    plugin.validators.cmd.validate("dir", search="test", allowed_return_codes=0)
    plugin.validators.cmd.validate("dir", search="test", allowed_return_codes=[0])
    plugin.validators.cmd.validate("dir", search="test", allowed_return_codes=[1, 2, 3, 0])
    plugin.validators.cmd.validate("exit 2", search="test", allowed_return_codes=[2])

    with pytest.raises(NotAllowedReturnCode):
        plugin.validators.cmd.validate("UNKNOWN_COMMAND", search="test", allowed_return_codes=[0])

    with pytest.raises(NotAllowedReturnCode):
        plugin.validators.cmd.validate("UNKNOWN_COMMAND", search="test", allowed_return_codes=0)


def test_cmd_validator_errors():
    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()

    with pytest.raises(ValueError):
        plugin.validators.cmd.validate("dir")

    with pytest.raises(ValueError):
        plugin.validators.cmd.validate("dir", search="test", regex="test")

    with pytest.raises(TypeError):
        plugin.validators.cmd.validate("dir", search="test", allowed_return_codes="123")


def test_cmd_validator_timeout():
    class My_Plugin(GwCmdValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    app = groundwork.App()
    plugin = My_Plugin(app)
    plugin.activate()

    plugin.validators.cmd.validate(_sleep(1), search="")
    with pytest.raises(CommandTimeoutExpired):
        plugin.validators.cmd.validate(_sleep(3), search="")

    plugin.validators.cmd.validate(_sleep(1), search="", timeout=2)
    with pytest.raises(CommandTimeoutExpired):
        plugin.validators.cmd.validate(_sleep(1), search="", timeout=0.5)


def _sleep(seconds):
    """
    Helper functions, which generates a sleep like command depending on which operating system
    theses tests are running.
    :param seconds:
    :return:
    """
    if os.name == 'nt':
        command = "ping 127.0.0.1 -n %s " % seconds + 1
    else:
        command = "sleep %s" % seconds

    return command
