from setuptools import setup

setup(
    name="TranslationManager",
    version="0.1",

    author="Pavel Cisar & Martin Kubat",
    author_email="cisarpavel@gmail.com",

    # Packages
    packages=["translation_manager"],

    # Include additional files into the package
    include_package_data=True,

    #
    license="license.txt",
    description="Django app for managing translations from admin",

    install_requires=[
        "polib",
        "django>=1.2"
    ],
)
