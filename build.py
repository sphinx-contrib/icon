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

        # create a _vendor folder
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
