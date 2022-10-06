"""
Setup.py file

Configure the project, build the package and upload the package to PYPI
"""
import setuptools
from Cython.Build import cythonize
from setuptools import Extension

# NUMPY IS REQUIRED
try:
    import numpy
except ImportError:
    raise ImportError("\n<numpy> library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ElasticCollision",
    version="1.0.5",          # Actual version on PyPI is 1.0.5, TEST is 1.0.13
    author="Yoann Berenguer",
    author_email="yoyoberenguer@hotmail.com",
    description="ElasticCollision tools for pygame and arcade games ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoyoberenguer/ElasticCollision",
    # packages=setuptools.find_packages(),
    packages=['ElasticCollision'],
    ext_modules=cythonize([
        Extension("ElasticCollision.ec_game", ["ElasticCollision/game/ec_game.pyx"],
                  extra_compile_args=["/openmp", "/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"],
                  language="c"),
        Extension("ElasticCollision.c_game", ["ElasticCollision/game/c_game.pyx"],
                  extra_compile_args=["/openmp", "/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"],
                  language="c"),
        Extension("ElasticCollision.ec_real", ["ElasticCollision/real/ec_real.pyx"],
                  extra_compile_args=["/openmp", "/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"],
                  language="c")]),
    include_dirs=[numpy.get_include()],
    # define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    license='MIT',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Cython',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires=[
        'setuptools>=49.2.1',
        'Cython>=0.28',
        'numpy>=1.18',
        'pygame>=2.0'
    ],
    python_requires='>=3.6',
    platforms=['any'],
    include_package_data=True,
    data_files=[
        ('./lib/site-packages/ElasticCollision',
         ['LICENSE',
          'MANIFEST.in',
          'pyproject.toml',
          'README.md',
          'requirements.txt',
          'simulation.py'
          ]),

        ('./lib/site-packages/ElasticCollision/game',
         [
             'ElasticCollision/game/__init__.py',
             'ElasticCollision/game/ec_game.pyx',
             'ElasticCollision/game/c_game.pyx',
             'ElasticCollision/game/setup_ec_game.py'
         ]
         ),
        ('./lib/site-packages/ElasticCollision/real',
         [
             'ElasticCollision/real/__init__.py',
             'ElasticCollision/real/ec_real.pyx',
             'ElasticCollision/real/setup_ec_real.py'
         ]
         ),

        ('./lib/site-packages/ElasticCollision/Assets',
         [
            'ElasticCollision/Assets/math1.png',
            'ElasticCollision/Assets/math2.png',
            'ElasticCollision/Assets/math3.png',
            'ElasticCollision/Assets/math4.png',
            'ElasticCollision/Assets/GameDomain.PNG',
            'ElasticCollision/Assets/RealDomain.PNG',
            'ElasticCollision/Assets/GameDomain_wrong_trajectory.PNG',


         ]),

        ('./lib/site-packages/ElasticCollision/tests',
         [
            'ElasticCollision/tests/test_ec_game.py',
            'ElasticCollision/tests/test_ec_real.py',
            'ElasticCollision/tests/__init__.py',

         ]),

        ('./lib/site-packages/ElasticCollision/Source',
         [
             'ElasticCollision/Source/elastic_collision.c',
             'ElasticCollision/Source/vector.c',


         ])
    ],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/yoyoberenguer/ElasticCollision/issues',
        'Source': 'https://github.com/yoyoberenguer/ElasticCollision',
    },
)

