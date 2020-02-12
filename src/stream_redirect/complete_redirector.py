import ctypes
import io
import os
import six
import sys
import tempfile
from ctypes.util import find_library


class CompleteRedirector(object):
    def __init__(self, src):
        self._src = src
        self._encoding = getattr(sys, self._src).encoding

    @property
    def libc(self):
        """
        The standard C library on target systems
        """
        if sys.platform.startswith('win'):
            if sys.version_info < (3, 5):
                return ctypes.CDLL(find_library('c'))
            else:
                if hasattr(sys, 'gettotalrefcount'):  # debug build
                    return ctypes.CDLL('ucrtbased')
                else:
                    return ctypes.CDLL('api-ms-win-crt-stdio-l1-1-0')
        else:
            return ctypes.CDLL(None)

    @property
    def _c_src(self):
        """
        The file descriptor for std{out,err} on the current system
        """
        if sys.platform.startswith('darwin'):
            return ctypes.c_void_p.in_dll(self.libc, '__{}p'.format(self._src))
        elif sys.platform.startswith('win'):
            kernel32 = ctypes.WinDLL('kernel32')
            # Magic numbers drawn from the Microsoft API
            # stdin is -10
            if self._src == "stdout":
                HANDLE = -11
            elif self._src == "stderr":
                HANDLE = -12
            return kernel32.GetStdHandle(HANDLE)
        else:
            return ctypes.c_void_p.in_dll(self.libc, self._src)

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
            self.output = six.ensure_str(self.tmpfile.read())
        finally:
            self.tmpfile.close()
            os.close(self._saved_fd)

    def _redirect_src(self, fd):
        if sys.platform.startswith('win'):
            self.libc.fflush(None)
        else:
            self.libc.fflush(self._c_src)
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
