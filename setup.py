from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'A tool for finding resources unmanaged by cloudformation'


setup(
    name="cfn-sweeper",
    version=VERSION,
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            'cfn_sweeper=cfn_sweeper.main:main',
        ],
    },
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'boto3',
        'wheel',
        'pyyaml',
        'pyfiglet'
    ],
    python_requires=">=3.8"
    
)
