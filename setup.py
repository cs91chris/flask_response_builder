"""
Flask-ResponseBuilder
-------------

Implementations of flask response in many formats like
"""
from setuptools import setup

from flask_response_builder import __version__
from flask_response_builder import __author__


author, email = __author__.split()
email = email.lstrip('<').rstrip('>')

with open("README.rst", "r") as rd:
    long_description = rd.read()


setup(
    name='Flask-ResponseBuilder',
    version=__version__,
    url='https://github.com/cs91chris/flask_response_builder',
    license='MIT',
    author=author,
    author_email=email,
    description='Implementations of flask response in many formats',
    long_description=long_description,
    packages=['flask_response_builder'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    tests_require=['pytest'],
    install_requires=[
        'Flask==1.0.2',
        'PyYAML==5.1',
        'xmltodict==0.12.0',
        'dicttoxml==1.7.4'
    ],
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
