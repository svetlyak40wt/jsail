#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'click',
    'anyjson',
    'tailer', # for python3 you need to take a version from the github: https://github.com/six8/pytailer
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='jsail',
    version='0.2.1',
    description="A tail for JSON logs.",
    long_description=readme + '\n\n' + history,
    author="Alexander Artemenko",
    author_email='svetlyak.40wt@gmail.com',
    url='https://github.com/svetlyak40wt/jsail',
    packages=[
        'jsail',
    ],
    package_dir={'jsail':
                 'jsail'},
    entry_points={
        'console_scripts': [
            'jsail = jsail:main_func',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='jsail',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
