from subprocess import check_output, CalledProcessError, STDOUT
from re import finditer

from groundwork_validation.patterns import GwValidatorsPattern


class GwCmdValidatorsPattern(GwValidatorsPattern):

    def __init__(self, app, **kwargs):
        super(GwCmdValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app
        self.validators.cmd = CmdValidatorsPlugin(self)


class CmdValidatorsPlugin:

    def __init__(self, plugin):
        self.plugin = plugin

    def validate(self, command, search=None, regex=None, timeout=2, allowed_return_codes=None, decode="utf-8"):
        if search is None and regex is None:
            raise ValueError("Parameter search or regex must be set.")
        if search is not None and regex is not None:
            raise ValueError("Only search OR regex is allowed to be used. Not both!")

        if allowed_return_codes is None:
            allowed_return_codes = []
        if isinstance(allowed_return_codes, int):
            allowed_return_codes = [allowed_return_codes]
        if not isinstance(allowed_return_codes, list):
            raise TypeError("allowed_return_code must be a list of integers")

        try:
            output = check_output(command, stderr=STDOUT, shell=True, timeout=timeout)
            return_code = 0
        except CalledProcessError as e:
            output = e.output
            return_code = e.returncode

        if len(allowed_return_codes) > 0 and return_code not in allowed_return_codes:
            raise NotAllowedReturnCode("For command %s got return code '%s', which is not in %s"
                                       % (command, return_code, allowed_return_codes))

        self.plugin.log.debug("Executed '%s' with return code: %s" % (command, return_code))

        output = output.decode(decode)
        found = False
        if search is not None:
            if search in output:
                found = True
        elif regex is not None:
            for m in finditer(regex, output):
                self.plugin.log.debug("Found cmd validation '%s' at %02d-%02d" % (m.group(0), m.start(), m.end()))
                found = True
        return found


class NotAllowedReturnCode(BaseException):
    pass
