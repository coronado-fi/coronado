#!/usr/bin/env python3
# vim: set fileencoding=utf-8:


import pathlib
import sys

from setuptools import find_packages
from setuptools import setup

from coronado import __VERSION__

# +++ constants +++

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()


# *** functions ***

def readToList(fileName):
    return [line.strip() for line in open(fileName).readlines()]


# *** main ***

if '__main__' == __name__:
    requirements = readToList('requirements.txt')

    setup(
        author                        = 'Eugene Ciurana pr3d4t0r',
        author_email                  = 'eugene.ciurana@numo.com',
        classifiers                   = [
            "Intended Audience :: Other Audience",
            "Operating System :: MacOS",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
        ],
        description                   = 'Coronado - triple API Python wrapper and reference implementation',
#         entry_points                  = {
#                                     'console_scripts': {
#                                         'coronado=coronado:main',
#                                     }
#                                },
        include_package_data          = True,
        install_requires              = requirements,
        license                       = "Apache 2.0",
        long_description              = README,
        long_description_content_type = 'text/markdown',
        name                          = open('package.txt').read().replace('\n', ''),
        namespace_packages            = [ ],
        packages                      = find_packages(),
        url                           = 'https://github.com/coronado-fi/coronado',
        version                       = __VERSION__,
    )

sys.exit(0)

