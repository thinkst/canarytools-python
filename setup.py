from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='canarytools',

    version='1.0.10',

    description='An API for the Thinkst Canary Console',
    long_description=long_description,

    url='https://canary.tools/',

    author='Thinkst Applied Research',
    author_email='canary@thinkst.com',

    license='Revised BSD License',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],

    keywords='canary thinkst canarytools api wrapper',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests>=2.10.0', 'python-dateutil>=2.1', 'pytz>=2013b'],

    package_data={
        '': ['LICENSE.txt'],
    },
)
