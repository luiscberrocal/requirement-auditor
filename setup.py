#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Luis C. Berrocal",
    author_email='luis.berrocal.1942@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Utility to revise and updated python requirement files.",
    entry_points={
        'console_scripts': [
            'requirement_auditor=requirement_auditor.cli:main',
            'db=requirement_auditor.db:main',

        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='requirement_auditor',
    name='requirement_auditor',
    packages=find_packages(include=['requirement_auditor', 'requirement_auditor.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luiscberrocal/requirement_auditor',
    version='0.1.0',
    zip_safe=False,
)
