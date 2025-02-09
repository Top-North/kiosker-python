from setuptools import find_packages, setup

setup(
    name='kioskerPython',
    packages=find_packages(),
    version='25.2.1',
    description='A python wrapper for the Kiosker API',
    author='Martin Claesson',
    install_requires=['httpx'],
    setup_requires=[],
    extras_require={
        'test': ['pytest'],
    },
)