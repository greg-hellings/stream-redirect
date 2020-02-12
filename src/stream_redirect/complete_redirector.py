import ctypes
import io
import os
import six
import sys
import tempfile


libc = ctypes.CDLL(None)


class CompleteRedirector(object):
    def __init__(self, src):
        self._src = src
        self._c_src = ctypes.c_void_p.in_dll(libc, self._src)
        self._encoding = getattr(sys, self._src).encoding

    def begin(self):
        # The original fd for the system stream
        self._original_fd = getattr(sys, self._src).fileno()
        self._saved_fd = os.dup(self._original_fd)
        # The file where we will direct output
        self.tmpfile = tempfile.TemporaryFile(mode="w+b")
        # Setup the actual redirect
        self._redirect_src(self.tmpfile.fileno())

    def end(self):
        try:
            self._redirect_src(self._saved_fd)
            # Save the contents of the written file
            self.tmpfile.flush()
            self.tmpfile.seek(0, io.SEEK_SET)
            self.output = self.tmpfile.read().decode(self._encoding)
        finally:
            self.tmpfile.close()
            os.close(self._saved_fd)

    def _redirect_src(self, fd):
        libc.fflush(self._c_src)
        # Close the stream, including the fd
        getattr(sys, self._src).close()
        # Make the original point to the same file as our target
        os.dup2(fd, self._original_fd)
        # Creates a new stream that points to the redirected fd
        if six.PY3:
            wrap = io.TextIOWrapper(os.fdopen(self._original_fd, "wb"))
        else:
            wrap = os.fdopen(self._original_fd, "wb")
        setattr(sys, self._src, wrap)
