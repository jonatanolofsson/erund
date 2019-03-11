#!/usr/bin/env python

from setuptools import setup

setup(name='erund',
      version='0.1',
      description='Distribute and execute software on embedded connected systems',
      author='Jonatan Olofsson',
      author_email='jonatan.olofsson@gmail.com',
      packages=['erund'],
      entry_points={'console_scripts': ['erund=erund.erund:main']})
