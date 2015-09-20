# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='memspector',
    version='0.1.2',
    description="Inspect memory usage of python functions",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    keywords='memory debugger inspector',
    author='Adam Tauber',
    author_email='asciimoo@gmail.com',
    url='https://github.com/asciimoo/memspector',
    license='GNU Affero General Public License',
    scripts=['memspector.py'],
    py_modules=['memspector'],
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    entry_points={
        "console_scripts": ["memspector=memspector:__main"]
    },
)
