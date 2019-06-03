"""Config for Pypi."""

from setuptools import setup, find_packages


DESCRIPTION = "Small piece of code to explore interface review tabular data."

setup(
    name='interface',
    author='Maud Ehrmann, Estelle Bunout, Marten Düring',
    author_email='maud.ehrmann@epfl.ch',
    url='https://github.com/impresso/impresso-interface-review',
    packages=find_packages(),
    long_description=DESCRIPTION,
    install_requires=[
        'jupyter',
        'numpy',
        'pandas',
        'matplotlib'
    ]
)
