import os
from distutils.core import setup

from setuptools import find_packages

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = "Python script to continuously analyze crypto data."

setup(
    name="admoneo",
    # Packages to include in the distribution:
    packages=find_packages("admoneo,"),
    # Project version number:
    version="0.0.1dev",
    # List a license for the project, eg. MIT License
    license="GNU",
    # Short description of your library:
    description="",
    # Long description of your library:
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Your name:
    author="artem dukhnitskiy",
    # Your email address:
    author_email="admoneo_bot@protonmail.com",
    # Link to your github repository or website:
    url="https://github.com/dukhniav/admoneo",
    # Download Link from where the project can be downloaded from:
    download_url="https://github.com/dukhniav/admoneo",
    # List of keywords:
    keywords=["crypto", "bot", "analyze", "analyzer", "twitter"],
    # List project dependencies:
    install_requires="requirements.txt",
    # https://pypi.org/classifiers/
    classifiers=[],
)
