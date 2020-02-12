"""
Since coverage.py 5 introduced the relative path option, it remains non-trivial
to combine results from Windows and Unix because of the difference in the
path separator. This script converts all instances of the '\' character in the
path to '/' and should be run prior to the combine step.
"""
# See https://github.com/nedbat/coveragepy/issues/903
import sys
import sqlite3


def main(argv):
    paths = argv[1:]

    for path in paths:
        # https://github.com/nedbat/coveragepy/issues/903
        conn = sqlite3.connect(path)
        conn.execute("UPDATE file set path = REPLACE(path, '\\', '/')")
        conn.commit()
        conn.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
