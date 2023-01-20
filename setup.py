#!/usr/bin/env python
from setuptools import setup, find_packages


def get_requirements():
    return open('requirements.txt').read().splitlines()


setup(name='testapp',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py'],
      install_requires=get_requirements()
      )
