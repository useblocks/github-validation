from subprocess import check_output, CalledProcessError

from groundwork_validation.patterns import GwValidatorsPattern


class GwFileValidatorsPattern(GwValidatorsPattern):

    def __init__(self, app, **kwargs):
        super(GwFileValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app
        self.validators.db = FileValidatorsPlugin(self)


class FileValidatorsPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self._validator = None

    def validate(self, file,  validator=None):

        if validator is None:
            if self._validator is None:
                self._validator = self.plugin.validators.register("cmd_validator_%s" % self.plugin.name,
                                                                  "CMD validator for plugin %s" % self.plugin.name)
            validator = self._validator

        try:
            output = check_output()
            return_code = 0
        except CalledProcessError as e:
            output = e.output
            return_code = e.returncode

