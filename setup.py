#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

import admin_top_models

version = admin_top_models.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return [r for r in (strip_comments(lr) for l in (open(os.path.join(os.getcwd(), ff)).readlines() for ff in f) for lr in l) if r]


readme = open('README.rst').read()
changelog = open('CHANGELOG.rst').read()

setup(
        name='django-admin-top-models',
        version=version,
        description="",  # todo
        long_description=readme + '\n\n' + changelog,
        author='Kostya Esmukov',
        author_email='kostya@esmukov.ru',
        url='https://github.com/KostyaEsmukov/django-admin-top-models',
        packages=[
            'admin_top_models',
        ],
        include_package_data=True,
        install_requires=reqs("requirements.txt"),
        license="LPGL",
        zip_safe=False,
        keywords='django modeladmin admin reorder top',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
)
