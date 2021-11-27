"""
SETUP EC_GAME.PYX
"""
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

ext_modules = cythonize([
    Extension("ec_real", ["ec_real.pyx"],
              extra_compile_args=["/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"], language="c")
    # Extension("c_real", ["c_real.pyx"],
    #           extra_compile_args=["/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"], language="c")])
])

setup(
    name="game",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()]
)
