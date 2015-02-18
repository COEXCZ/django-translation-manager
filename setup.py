# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "translation_manager"
NAME = "django-translation-manager"
DESCRIPTION = "Django app for managing translations from admin"
AUTHOR = "Pavel Císař, Martin Kubát, Mikuláš Mrva, COEX CZ s.r.o (http://www.coex.cz)"
AUTHOR_EMAIL = "cisarpavel@gmail.com"
URL = "https://github.com/COEXCZ/django-translation-manager"
VERSION = '0.2.0'
LICENSE = "CC BY-NC 3.0"

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
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Internationalization"
    ],
    install_requires=[
        "polib",
        "django>=1.2"
    ],
)