# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "translation_manager"
NAME = "django-translation-manager"
DESCRIPTION = "Django app for managing translations from admin"
AUTHOR = "Pavel Císař, Martin Kubát, Mikuláš Mrva, Jakub Ladra, Michal Kašpar, Jan Češpivo - COEX CZ s.r.o (http://www.coex.cz)"
AUTHOR_EMAIL = "pavel.cisar@coex.cz"
URL = "https://github.com/COEXCZ/django-translation-manager"
VERSION = '1.0.0'
LICENSE = "Mozilla Public License 2.0 (MPL 2.0)"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=["translation_manager"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Internationalization"
    ],
    install_requires=[
        "polib",
        "django>=1.8",
        "djangorestframework>=3.7.1",
        "requests>=2.18.4",
    ],
    test_suite="runtests.run_tests",
)
