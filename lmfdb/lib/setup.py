"""
Build instructions:

First, generate C source files from pari_bnr.pyx:

SAGE=/Applications/Sage-4.8-OSX-64bit-10.6.app/Contents/Resources/sage
sage -cython -p -a --pre-import sage.all -I "$SAGE/devel/sage" \
                                         -I "$SAGE/local/include/csage" \
pari_bnr.pyx
#-I '/home/vbraun/Code/sage/src' -I'/home/vbraun/Code/sage/include/csage'
Second, build using this setup.py script:

sage -python setup.py build

The output is then in 

./build/lib.<os>/pari_bnr.so
"""

import distutils.sysconfig, os, sys
from distutils.core import setup, Extension

from sage.env import SAGE_ROOT, SAGE_LOCAL

from setuptools import setup, Extension
from Cython.Distutils import build_ext

extra_link_args =  ['-L' + SAGE_LOCAL + '/lib', '-lgmp', '-lpari']
extra_compile_args = ['-I'+ SAGE_LOCAL + '/include/csage']

ext_modules = [Extension('pari_bnr', sources=['pari_bnr.c'],
                         library_dirs=[SAGE_LOCAL + '/lib/'],
                         libraries=['csage'],
                         extra_compile_args=extra_compile_args,
                         extra_link_args=extra_link_args,
                         language='c' )]
include_dirs = [SAGE_ROOT + "/local/include/csage/",
                SAGE_ROOT + "/local/include/",
                SAGE_ROOT + "/local/include/python2.7",]

setup(name='pari_bnr',
      author='Pascal Molin',
      author_email='molin.maths@gmail.com',
      ext_modules = ext_modules,
      include_dirs=include_dirs)
