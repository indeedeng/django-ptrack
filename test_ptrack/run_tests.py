#!/usr/bin/env python
# encoding: utf-8
import sys
from os.path import abspath, dirname
import nose
from pylint import epylint as lint

def run_all(argv=None):
    sys.exitfunc = lambda: sys.stderr.write('Shutting down....\n')

    pylint_stdout, pylint_stderr = lint.py_run('ptrack', return_std=True)
    print(pylint_stdout.getvalue())
    print(pylint_stderr.getvalue())


    if argv is None:
        argv = [
            'nosetests', '--with-coverage', '--cover-package=ptrack',
            '--cover-erase', '--verbose',
        ]

    nose.run_exit(
        argv=argv,
        defaultTest=abspath(dirname(__file__))
    )


if __name__ == '__main__':
    run_all(sys.argv)
