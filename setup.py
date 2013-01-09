#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

setup(
    name='facebook-datastore',
    version='0.2',
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
    ),
    packages=find_packages(),
    include_package_data=True,
)
