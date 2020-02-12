from __future__ import print_function
import os
import six
import sys
from unittest import TestCase
from stream_redirect import Redirect
from stream_redirect.complete_redirector import CompleteRedirector


class TestStderr(TestCase):
    @classmethod
    def setUpClass(self):
        self.libc = CompleteRedirector("stdout").libc

    def test_gets_python_output(self):
        """
        Tests that only ouptut from the Python code will be collected and not
        anything from system calls or from the underlying C library code.
        """
        expected_output = "Some string"
        stdout_not_found = "stdout string"
        not_found = "not found"
        also = "also not found"
        # Do the attempt
        cm = Redirect(python_only=True, stderr=True, stdout=False)
        with cm:
            print(expected_output, file=sys.stderr)
            print(stdout_not_found)
            os.system("echo {not_found}")
            self.libc.puts(six.ensure_binary(also))
        self.assertIn(expected_output, cm.stderr)
        self.assertNotIn(stdout_not_found, cm.stderr)
        self.assertNotIn(not_found, cm.stderr)
        self.assertNotIn(also, cm.stderr)

    def test_gets_all_output(self):
        """
        Tests that all things written out by the code are collected in the
        context manager object
        """
        py_out = "python string"
        sys_call = "system call"
        c_code = "c code"
        # Make the attempt
        cm = Redirect(stderr=True, stdout=False)
        with cm:
            print(py_out, file=sys.stderr)
            os.system("echo {} 1>&2".format(sys_call))
            self.libc.puts(six.ensure_binary(c_code))
        self.assertIn(py_out, cm.stderr)
        self.assertIn(sys_call, cm.stderr)
        self.assertNotIn(c_code, cm.stderr)  # puts still doesn't go to stderr
