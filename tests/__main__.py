import unittest
import sys
from . import test_stderr, test_stdout

if __name__ == "__main__":
    loader = unittest.TestLoader()
    # Tests that don't need to be modified
    default_suite = unittest.TestSuite()
    default_suite.addTests(loader.loadTestsFromModule(test_stdout))
    unittest.TextTestRunner().run(default_suite)
    # These need to be run differently
    modified_suite = unittest.TestSuite()
    modified_suite.addTests(loader.loadTestsFromModule(test_stderr))
    unittest.TextTestRunner(stream=sys.stdout).run(modified_suite)
