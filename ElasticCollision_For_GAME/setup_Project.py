# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp


# USE :
# python setup_Project.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


ext_modules = [

    Extension("EC_SHARED", ["EC_SHARED.pyx"],
              include_dirs=[numpy.get_include()],
              extra_compile_args=['/openmp'],
              extra_link_args=['/openmp']),

    Extension("EC_GAME", ["EC_GAME.pyx"],
              include_dirs=[numpy.get_include()],
              extra_compile_args=['/openmp'],
              extra_link_args=['/openmp']),

    Extension("ECC", ["ECC.pyx"],
              include_dirs=[numpy.get_include()],
              extra_compile_args=['/openmp'],
              extra_link_args=['/openmp'])


]

setup(
    name="EC_GAME",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()]
)
