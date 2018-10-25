from distutils.core import setup
from Cython.Build import cythonize

setup(name='csyst',
      ext_modules=cythonize("csyst.py"))

setup(name='csyst',
      ext_modules=cythonize("cpack.py"))
	  
setup(name='csyst',
      ext_modules=cythonize("cmath.py"))
	  
