from setuptools import setup

setup(
    name = 'simpletar',
    version = '0.1.0',
    description = 'A simple command-line wrapper around the "tar" utility',
    url = 'https://github.com/VHarisop/Simpletar',
    author = 'VHarisop',
    license = 'GPLv3',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Anyone',
        'Programming Language :: Python :: 3'
    ],

    packages = [
        'simpletar'
    ],

    entry_points = {
        'console_scripts': [
            'simpletar = simpletar.simpletar:main',
        ]
    }
)
