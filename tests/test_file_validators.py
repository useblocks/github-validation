import pytest
import groundwork
from groundwork_validation.patterns import GwFileValidatorsPattern


def test_file_validator_init():
    class My_Plugin(GwFileValidatorsPattern):
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


def test_file_validator_hash(tmpdir):
    test_file_1 = tmpdir.mkdir("sub_1").join("test_1.txt")
    test_file_1.write("content")

    test_file_2 = tmpdir.mkdir("sub_2").join("test_2.txt")
    test_file_2.write("content")

    test_file_3 = tmpdir.mkdir("sub_3").join("test_2.txt")
    test_file_3.write("content_3")

    class My_Plugin(GwFileValidatorsPattern):
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

    hash_1 = plugin.validators.file.hash(test_file_1.strpath)
    assert hash_1 is not None

    hash_2 = plugin.validators.file.hash(test_file_2.strpath)
    assert hash_2 is not None
    assert hash_1 == hash_2

    hash_3 = plugin.validators.file.hash(test_file_3.strpath)
    assert hash_3 is not None
    assert hash_3 != hash_1

    hash_object_1 = plugin.validators.file.hash(test_file_1.strpath, return_hash_object=True)
    assert hash_object_1 is not None

    hash_1_file = tmpdir.join("sub_1", "test_1.hash").strpath
    hash_1 = plugin.validators.file.hash(test_file_1.strpath, hash_file=hash_1_file)
    with open(hash_1_file, "r") as hash_1_fobject:
        assert hash_1_fobject.readline() == hash_1


def test_file_validator_validate(tmpdir):
    test_file_1 = tmpdir.mkdir("sub_1").join("test_1.txt")
    test_file_1.write("content")

    class My_Plugin(GwFileValidatorsPattern):
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

    test_file_1_hash = tmpdir.join("sub_1", "test_1.hash")
    test_1_hash = plugin.validators.file.hash(test_file_1.strpath)
    test_file_1_hash.write(test_1_hash)

    assert plugin.validators.file.validate(test_file_1.strpath, test_1_hash) is True
    assert plugin.validators.file.validate(test_file_1.strpath, "NoWay") is False

    assert plugin.validators.file.validate(test_file_1.strpath, hash_file=test_file_1_hash.strpath) is True
    assert plugin.validators.file.validate(test_file_1.strpath,
                                           hash_file=test_file_1_hash.strpath, blocksize=1024) is True

    test_file_1_no_hash = tmpdir.join("sub_1", "test_1.no_hash")
    test_file_1_no_hash.write("NoWay")
    assert plugin.validators.file.validate(test_file_1.strpath, hash_file=test_file_1_no_hash.strpath) is False


def test_file_validator_validate_errors(tmpdir):
    test_file_1 = tmpdir.mkdir("sub_1").join("test_1.txt")
    test_file_1.write("content")

    class My_Plugin(GwFileValidatorsPattern):
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
        plugin.validators.file.validate(test_file_1.strpath)

    with pytest.raises(ValueError):
        plugin.validators.file.validate(test_file_1.strpath, "No", "NoFilePath")

    with pytest.raises(FileNotFoundError):
        plugin.validators.file.validate(test_file_1.strpath, hash_file="NoFilePath")
