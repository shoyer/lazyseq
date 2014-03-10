import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lazyseq",
    version="0.1.1",
    author="Stephan Hoyer",
    description="a lazily evaluated sequence type for Python",
    license="MIT",
    keywords="lazy seq sequence",
    url="http://github.com/shoyer/lazyseq",
    py_modules=['lazyseq'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
