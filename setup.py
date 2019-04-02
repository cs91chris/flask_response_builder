"""
Flask-ResponseBuilder
-------------

Implementations of flask response in many formats like
"""
from setuptools import setup


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='Flask-ResponseBuilder',
    version='1.0.0',
    url='https://github.com/cs91chris/flask_response_builder',
    license='MIT',
    author='cs91chris',
    author_email='cs91chris@voidbrain.me',
    description='Implementations of flask response in many formats',
    long_description=long_description,
    packages=['flask_response_builder'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
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
