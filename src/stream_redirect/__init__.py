from .simple_redirector import SimpleRedirector
from .complete_redirector import CompleteRedirector


class Redirect(object):
    def __init__(self, python_only=False, stdout=True, stderr=False):
        self.redirectors = {}
        if stdout:
            if python_only:
                self.redirectors["stdout"] = SimpleRedirector("stdout")
            else:
                self.redirectors["stdout"] = CompleteRedirector("stdout")
        if stderr:
            if python_only:
                self.redirectors["stderr"] = SimpleRedirector("stderr")
            else:
                self.redirectors["stderr"] = CompleteRedirector("stderr")

    def __enter__(self):
        for r in self.redirectors.values():
            r.begin()

    def __exit__(self, ex_type, ex, ex_tb):
        for r in self.redirectors.values():
            r.end()
        return False

    @property
    def stdout(self):
        try:
            return self.redirectors["stdout"].output
        except KeyError:
            raise NotImplementedError("stdout capture not requested")

    @property
    def stderr(self):
        try:
            return self.redirectors["stderr"].output
        except KeyError:
            raise NotImplementedError("stderr capture not requested")
