from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='PHYSICS',
    ext_modules=cythonize(["*.pyx"]), requires=['pygame']
)
