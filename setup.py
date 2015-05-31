from setuptools import setup, find_packages

from rocketsled import __version__


setup(
    name='rocketsled',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'boto==2.38.0',
    ],
    entry_points = {
        'console_scripts': ['rocketsled=rocketsled.__main__:main'],
    }
)
