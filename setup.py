"""
Flask-ResponseBuilder
-------------

Implementations of flask response in many formats: base64, csv, json, xml, html, yaml
"""
import sys
import pytest

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test

from flask_response_builder import __version__
from flask_response_builder import __author__


author, email = __author__.split()
email = email.lstrip('<').rstrip('>')

with open("README.rst", "r") as rd:
    long_description = rd.read()


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)

    def run_tests(self):
        sys.exit(pytest.main(['tests']))


setup(
    name='Flask-ResponseBuilder',
    version=__version__,
    url='https://github.com/cs91chris/flask_response_builder',
    license='MIT',
    author=author,
    author_email=email,
    description='Implementations of flask response in many format notation',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    tests_require=[
        'pytest==4.5.0',
        'pytest-cov==2.7.1'
    ],
    install_requires=[
        'Flask==1.0.2',
        'PyYAML==5.1',
        'xmltodict==0.12.0',
        'dicttoxml==1.7.4'
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
