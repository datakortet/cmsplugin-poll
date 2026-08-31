from setuptools import setup, find_packages
import os

setup(
    name = "cmsplugin-poll",
    packages = find_packages(),
    version = "0.8.0",
    description = "Simple poll plugin for django-cms",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author = "Antoine Nguyen",
    author_email = "tonio@ngyn.org",
    url = "http://bitbucket.org/tonioo/cmsplugin-poll",
    license = "BSD",
    keywords = ["django", "django-cms", "poll"],
    classifiers = [
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django"
        ],
    include_package_data = True,
    python_requires = ">=3.10",
    install_requires = [
        # floors are the oldest combination the test matrix covers
        # (hop 0); no ceiling -- hop 7 runs Django 6.1 / django-cms 5.1.1
        'Django >= 2.2',
        'django-cms >= 3.7',
        ],
) 
