import setuptools
from setuptools.command.develop import develop
from subprocess import check_call


class DevelopCmd(develop):
    def run(self):
        """overwrite run command to install pre-commit hooks in dev mode"""
        check_call(["pre-commit", "install", "-t", "pre-commit", "-t", "commit-msg"])
        super().run()

        return


# set the version number
version = "0.1.0"

# set some text as CONST variables for readability
DESCRIPTION = "A sphinx custom role to embed inline fontawesome incon in the latex and html outputs"
LONG_DESCRIPTION = open("README.rst").read()

setup_params = {
    # metadata
    "name": "sphinx-icon",
    "version": version,
    "license": "BSD 2-Clause",
    "description": DESCRIPTION,
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/x-rst",
    "author": "Pierrick Rambaud",
    "author_email": "pierrick.rambaud49@gmail.com",
    "url": "https://github.com/12rambau/sphinx-icon",
    "download_url": f"https://github.com/12rambau/sepal_ui/archive/v{version}.tar.gz",
    "keywords": ["skeleton", "Python"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # options
    "python_requires": ">=3.6.9",
    "packages": setuptools.find_packages(),
    "include_package_data": True,
    "namespace_packages": ["sphinxcontrib"],
    "install_requires": ["Deprecated", "docutils", "pyyaml"],
    "cmdclass": {"develop": DevelopCmd},
    # extras_require
    "extras_require": {
        "dev": ["pre-commit", "commitizen"],
        "test": ["coverage", "pytest"],
        "doc": [
            "Sphinx",
            "sphinxcontrib-spelling",
            "sphinx-copybutton",
            "furo",
        ],
    },
}

setuptools.setup(**setup_params)
