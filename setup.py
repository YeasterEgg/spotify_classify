# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
  readme = f.read()

with open('LICENSE.md') as f:
  license = f.read()

setup(
  name='spotify_mood',
  version='0.1',
  description='REST API server for spotify mood',
  long_description=readme,
  author='Luca Mattiazzi',
  author_email='l.d.mattiazzi@gmail.com',
  url='https://yegg.it',
  license=license,
  packages=find_packages(exclude=('tests', 'docs'))
)
