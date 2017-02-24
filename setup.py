from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='nail-ssg',
    version='0.2',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'ruamel.yaml==0.13.14'
    ])
