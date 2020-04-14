"""
Flask-ResponseBuilder
-------------
"""
import sys

import pytest
from setuptools.command.test import test
from setuptools import setup, find_packages

from flask_response_builder import __version__, __author_info__

with open("README.rst") as rd:
    long_description = rd.read()


class PyTest(test):
    def finalize_options(self):
        """

        """
        test.finalize_options(self)

    def run_tests(self):
        """

        """
        sys.exit(pytest.main(['tests']))


setup(
    name='Flask-ResponseBuilder',
    version=__version__,
    url='https://github.com/cs91chris/flask_response_builder',
    license='MIT',
    author=__author_info__['name'],
    author_email=__author_info__['email'],
    description='Implementations of flask response in many format notation',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    tests_require=[
        'pytest==5.4.*',
        'pytest-cov==2.8.*'
    ],
    install_requires=[
        'Flask==1.1.*',
        'PyYAML==5.*',
        'xmltodict==0.12.*',
        'dicttoxml==1.7.*'
    ],
    cmdclass={'test': PyTest},
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
