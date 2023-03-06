import numpy
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("Fisher.pyx"),
    include_dirs=[numpy.get_include()]#,
    # compiler_directives={'language_level' : "3"}   # or "2" or "3str"
)

# to do:
# python setup.py build_ext --inplace