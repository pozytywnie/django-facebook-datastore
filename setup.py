#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup
import sys

setup(
    name='facebook-datastore',
    version='3.0.1',
    description="Facebook Datastore",
    maintainer="Tomasz Wysocki",
    maintainer_email="tomasz@wysocki.info",
    install_requires=(
        'django>=1.4',
        'facebook-javascript-authentication',
        'facebook-javascript-sdk',
        'factory-boy',
        'isodate',
        'south>=0.7.5',
    ) + (('mock',) if sys.version_info.major < 3 else ()),
    packages=find_packages(),
    include_package_data=True,
)
