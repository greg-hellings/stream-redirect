import unittest
import sys
from . import test_stderr, test_stdout

if __name__ == "__main__":
    do_exit = False
    loader = unittest.TestLoader()
    # Tests that don't need to be modified
    default_suite = unittest.TestSuite()
    default_suite.addTests(loader.loadTestsFromModule(test_stdout))
    def_res = unittest.TextTestRunner().run(default_suite)
    if def_res.errors or def_res.failures:
        do_exit = True
    # These need to be run differently
    modified_suite = unittest.TestSuite()
    modified_suite.addTests(loader.loadTestsFromModule(test_stderr))
    mod_res = unittest.TextTestRunner(stream=sys.stdout).run(modified_suite)
    if mod_res.errors or mod_res.failures or do_exit:
        sys.exit(1)
