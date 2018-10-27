from distutils.core import setup
from Cython.Build import cythonize

setup(name='csyst',
      ext_modules=cythonize("units.py"))

setup(name='csyst',
      ext_modules=cythonize("cmath.py"))

setup(name='csyst',
      ext_modules=cythonize("ndict.py"))
	  
setup(name='csyst',
      ext_modules=cythonize("verrs.py"))
	  
setup(name='csyst',
      ext_modules=cythonize("si.py"))
	  
setup(name='csyst',
      ext_modules=cythonize("ce.py"))