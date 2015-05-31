from setuptools import setup, find_packages

setup(
    name='rocketsled',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto==2.38.0',
    ],
    entry_points = {
        'console_scripts': ['rocketsled=rocketsled.__main__:main'],
    }
)
