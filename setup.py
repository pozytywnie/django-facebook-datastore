#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup
import sys

setup(
    name='facebook-datastore',
    version='3.0.3',
    description="Facebook Datastore",
    maintainer="Tomasz Wysocki",
    maintainer_email="tomasz@wysocki.info",
    install_requires=(
        'django>=1.4',
        'factory-boy',
        'isodate',
    ) + (('mock',) if sys.version_info.major < 3 else ()),
    packages=find_packages(),
)
