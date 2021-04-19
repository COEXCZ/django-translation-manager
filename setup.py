# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "translation_manager"
NAME = "django-translation-manager"
DESCRIPTION = "Django app for managing translations from admin"
AUTHOR = "Pavel Císař, Martin Kubát, Mikuláš Mrva, Jakub Ladra, Michal Kašpar, Jan Češpivo - COEX s.r.o (http://www.coex.cz)"
AUTHOR_EMAIL = "pavel.cisar@coex.cz"
URL = "https://github.com/COEXCZ/django-translation-manager"
VERSION = '1.1.1'
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
        "django>=2.2.20",
        "djangorestframework>=3.7.1",
        "requests>=2.18.4",
        "django-rq==2.4.1",
    ],
    test_suite="runtests.run_tests",
)
