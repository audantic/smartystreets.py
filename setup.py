#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

version = '0.4.2'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = [
    'requests>=2.0.0',
]

test_requirements = [
    'mock>=1.0.0',
    'responses==0.3.0',
]

# grequests isn't available on python 3, unfortunately, but make it a testing requirement
# if we are on python 2.
if int(sys.version[0]) == 2:
    test_requirements.append('grequests')


setup(
    name='smartystreets.py',
    version=version,
    description='A wrapper for the SmartyStreets address validation and geolocation API"',
    long_description=readme + '\n\n' + history,
    url='https://github.com/audantic/smartystreets.py',
    packages=['smartystreets'],
    package_dir={'smartystreets':
                 'smartystreets'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='smarty streets',
    test_suite='tests',
    tests_require=test_requirements,
)
