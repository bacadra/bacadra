from distutils.core import setup
from Cython.Build import cythonize

setup(name='verrs',
      ext_modules=cythonize("verrs.py"))

setup(name='csyst',
      ext_modules=cythonize("units.py"))

setup(name='csyst',
      ext_modules=cythonize("ndict.py"))
	  
setup(name='csyst',
      ext_modules=cythonize("nprec.py"))
