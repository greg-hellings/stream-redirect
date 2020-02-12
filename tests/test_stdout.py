from __future__ import print_function
import ctypes
import os
import six
import sys
from unittest import TestCase
from stream_redirect import Redirect


class TestStdout(TestCase):
    def test_gets_python_output(self):
        """
        Tests that only ouptut from the Python code will be collected and not
        anything from system calls or from the underlying C library code.
        """
        expected_output = "Some string"
        stderr_not_found = "stderr string"
        not_found = "not found"
        also = "also not found"
        # Write directly out from C code
        libc = ctypes.CDLL(None)
        # Do the attempt
        cm = Redirect(python_only=True)
        with cm:
            print(expected_output)
            print(stderr_not_found, file=sys.stderr)
            os.system("echo {not_found}")
            libc.puts(six.ensure_binary(also))
        self.assertIn(expected_output, cm.stdout)
        self.assertNotIn(stderr_not_found, cm.stdout)
        self.assertNotIn(not_found, cm.stdout)
        self.assertNotIn(also, cm.stdout)

    def test_gets_all_output(self):
        """
        Tests that all things written out by the code are collected in the
        context manager object
        """
        py_out = "python string"
        sys_call = "system call"
        c_code = "c code"
        libc = ctypes.CDLL(None)
        # Make the attempt
        cm = Redirect()
        with cm:
            print(py_out)
            os.system("echo {}".format(sys_call))
            libc.puts(six.ensure_binary(c_code))
        self.assertIn(py_out, cm.stdout)
        self.assertIn(sys_call, cm.stdout)
        self.assertIn(c_code, cm.stdout)

    def test_raises_errors(self):
        cm = Redirect()
        with self.assertRaises(NotImplementedError):
            cm.stderr
        cm = Redirect(stdout=False)
        with self.assertRaises(NotImplementedError):
            cm.stdout
