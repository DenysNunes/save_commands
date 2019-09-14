#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='save commands',
      version='0.1',
      description='Tool for save and run shell commands',
      author='Denys Gonzaga',
      author_email='denys.nunes.gonzaga@gmail.com',
      scripts=['bin/save-commands'],
      packages=find_packages(),
      test_suite='pytest',
      )
