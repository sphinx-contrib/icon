import setuptools
from setuptools.command.develop import develop
from distutils.command.install import install
from subprocess import check_call
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from pathlib import Path
from shutil import rmtree

# the fontawesome information
font_version = "5.15.4"
github_asset = f"https://github.com/FortAwesome/Font-Awesome/releases/download/{font_version}/fontawesome-free-{font_version}-{{}}.zip"


class DevelopCmd(develop):
    def run(self):
        """overwrite run command to install pre-commit hooks in dev mode"""
        check_call(["pre-commit", "install", "-t", "pre-commit", "-t", "commit-msg"])
        super().run()

        return


class InstallCmd(install):
    def run(self):
        """overwrite run command to install fontawsome package"""

        # create a var folder
        vendor_dir = Path(__file__).parent / "var"
        vendor_dir.mkdir(exist_ok=True)

        # install them in the vendor folder
        # and write down the folders name in the lib file
        for name in ["desktop", "web"]:

            # create the var dir
            dir = vendor_dir / name
            dir.mkdir(exist_ok=True)

            # flush it from previous installation
            rmtree(dir)

            # read the zipfile
            resp = urlopen(github_asset.format(name))
            zip_file = ZipFile(BytesIO(resp.read()))
            for file in zip_file.namelist():

                if Path(file).suffix == "":
                    continue

                # get the data
                data = zip_file.read(file)

                # create the appropriate folder if needed
                src_name = Path(file).name
                src_dir = Path(*Path(file).parts[1:-1])
                dst_dir = dir / src_dir
                dst_dir.mkdir(exist_ok=True, parents=True)
                dts_file = dst_dir / src_name
                dts_file.write_bytes(data)

        super().run()

        return


# set the version number
version = "0.0.0"

# set some text as CONST variables for readability
DESCRIPTION = "A sphinx custom role to embed inline fontawesome incon in the latex and html outputs"
LONG_DESCRIPTION = open("README.rst").read()

setup_params = {
    # metadata
    "name": "sphinxcontrib-icon",
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
        "License :: OSI Approved :: BSD-2-Clause",
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
    "install_requires": ["Deprecated"],
    "cmdclass": {"develop": DevelopCmd, "install": InstallCmd},
    # extras_require
    "extras_require": {
        "dev": ["pre-commit", "commitizen"],
        "test": ["coverage", "pytest"],
        "doc": ["Sphinx", "sphinxcontrib-spelling", "sphinx-copybutton"],
    },
}

setuptools.setup(**setup_params)
