from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A tool for finding resources unmanaged by cloudformation'


setup(
    name="cfn-sweeper",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'boto3'
    ]
)