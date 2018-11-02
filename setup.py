import sys
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    sys.exit('Sorry, Python < 3.5 is not supported')

setuptools.setup(
    name="bacadra",
    version="v0.2a",
    author="bacadra",
    author_email="bacadra@gmail.com",
    description="FEM package for Civil Engineering task's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.facebook.com/bacadra",
    download_url="https://github.com/bacadra",
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "dxfgrabber",
        "IPython",
        "regex",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)