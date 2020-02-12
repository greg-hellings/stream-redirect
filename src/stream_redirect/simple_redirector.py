import six
import sys


class SimpleRedirector(object):
    def __init__(self, src):
        self._src = src

    def begin(self):
        self._original = getattr(sys, self._src)
        self._dest = six.StringIO()
        setattr(sys, self._src, self._dest)

    def end(self):
        setattr(sys, self._src, self._original)
        self.output = self._dest.getvalue()
        self._dest.close()
