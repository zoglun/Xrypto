#!/usr/bin/env python

from setuptools import setup
import sys


if sys.version_info < (3,):
    print("hydra-crypto requires Python version >= 3.0")
    sys.exit(1)

setup(name='hydra-crypto',
      packages = ["arbitrage"],
      version='0.3',
      description='opportunity detector and automated trading',
      author='Phil Song',
      author_email='songbohr@gmail.com',
      url='https://github.com/philsong/hydra',
      arbitrage=['bin/hydra'],
      test_suite='nose.collector',
      tests_require=['nose'],
  )
