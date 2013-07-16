#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

setup(
    name='oscar-ecard',
    version='0.2',
    description="eCard payment system",
    maintainer="Tomasz Wysocki",
    maintainer_email="tomasz@wysocki.info",
    packages=find_packages(),
    include_package_data=True,
)
