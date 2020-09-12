"""
Author: LanHao
Date:2020/9/12
Python: python 3.6
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules = [Extension("Trees", ["Trees.pyx"])]
setup(
    name="Trees",
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(ext_modules,annotate=True),
)
