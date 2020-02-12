import ctypes
import io
import os
import sys
import tempfile


libc = ctypes.CDLL(None)


class CompleteRedirector(object):
    def __init__(self, src):
        self._src = src
        self._c_src = ctypes.c_void_p.in_dll(libc, self._src)
        self._original = getattr(sys, self._src)

    def begin(self):
        self._original_fd = getattr(sys, self._src).fileno()
        self._saved_fd = os.dup(self._original_fd)
        self.tmpfile = tempfile.TemporaryFile(mode="w+b")
        self._redirect_src(self.tmpfile.fileno())

    def end(self):
        self._redirect_src(self._saved_fd)
        self.tmpfile.flush()
        self.tmpfile.seek(0, io.SEEK_SET)
        self.output = self.tmpfile.read().decode(self._original.encoding)
        self.tmpfile.close()

    def _redirect_src(self, fd):
        libc.fflush(self._c_src)
        getattr(sys, self._src).close()
        os.dup2(fd, self._original_fd)
        wrap = io.TextIOWrapper(os.fdopen(self._original_fd, "wb"))
        setattr(sys, self._src, wrap)
