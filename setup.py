#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='FastSFC',
    version='0.1.0',
    description="",
    author="FastSFC",
    author_email='hello@fastsfc.com',
    url='',
    packages=find_packages(),
    package_data={'fastsfc': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
