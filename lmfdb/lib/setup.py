"""
Build instructions:

sage -python setup.py build

The output is then in 

./build/lib.<os>/pari_bnr.so
"""

import distutils.sysconfig, os, sys
from distutils.core import setup, Extension
import subprocess

from sage.env import SAGE_ROOT, SAGE_LOCAL, SAGE_SRC

from setuptools import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import Cython.Compiler.Options
import Cython.Compiler.Main

if len(sys.argv) > 1 and sys.argv[1] == "sdist":
    sdist = True
else:
    sdist = False


extra_compile_args = [
    '-I'+ SAGE_SRC,
    '-I'+ os.path.join(SAGE_LOCAL, 'include', 'csage'),
]

ext_modules = [
    Extension('pari_bnr', 
              sources=['pari_bnr.c'],
              library_dirs=[SAGE_LOCAL + '/lib/'],
              libraries=['csage', 'gmp', 'pari'],
              extra_compile_args=extra_compile_args,
              language='c' )
]

include_dirs = [
    SAGE_SRC,
    SAGE_LOCAL + "/include/",
    SAGE_LOCAL + "/include/csage/",
    SAGE_LOCAL + "/include/python2.7",
]


if not sdist:
    print 'Cythonizing...'
    cmd = ['cython', '-p', '-v', '--pre-import', 'sage.all']
    cmd += extra_compile_args
    cmd += ['pari_bnr.pyx']
    subprocess.check_call(cmd)
    print '... finished, C source code created.'
    

code = setup(name='pari_bnr',
             author='Pascal Molin',
             author_email='molin.maths@gmail.com',
             ext_modules=ext_modules,
             include_dirs=include_dirs)
