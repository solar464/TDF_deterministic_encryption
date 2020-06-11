try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Build import cythonize

ext_modules = [Extension('floodberry_ed25519',
                        sources = ['ge25519_arithmetic.pyx'])]

setup(name = 'floodberry_ed25519',
      ext_modules = cythonize(ext_modules, language_level =3))
