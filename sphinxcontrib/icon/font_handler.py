"""Handler to install the fontawesome resources in the build."""

from io import BytesIO
from pathlib import Path
from shutil import rmtree
from typing import Dict
from urllib.request import urlopen
from zipfile import ZipFile

from yaml import safe_load


class Fontawesome:
    """Class wrapper to deal with fontawesome based icons."""

    FONT_VERSION = "5.15.4"
    ASSET = "https://github.com/FortAwesome/Font-Awesome/releases/download/{version}/fontawesome-free-{version}-{type}.zip"
    TYPES = {"html": "web", "latex": "desktop"}

    icons_metadata = None
    dir = None

    def download_asset(self, format: str, path: Path) -> None:
        """Download the font assets from fontawsome distribution to the set path.

        Args:
            format: format of the output (html or latex)
            path: the destination directory (folder need to exist)
        """
        type = self.TYPES[format]
        asset = self.ASSET.format(version=self.FONT_VERSION, type=type)

        self.dir = path / "fontawesome"
        self.dir.mkdir(exist_ok=True, parents=True)
        rmtree(self.dir)

        # read the zip
        resp = urlopen(asset)
        zip_file = ZipFile(BytesIO(resp.read()))
        for file in zip_file.namelist():

            if Path(file).suffix not in [".css", ".js"]:
                continue

            # get the data
            data = zip_file.read(file)

            # create the appropriate folder if needed
            src_name = Path(file).name
            src_dir = Path(*Path(file).parts[1:-1])
            dst_dir = self.dir / src_dir
            dst_dir.mkdir(exist_ok=True, parents=True)
            dts_file = dst_dir / src_name
            dts_file.write_bytes(data)

    def get_metadata(self) -> Dict[str, str]:
        """Read yaml file to create a datatable of existing icons.

        Returns:
            the stored table if existing
        """
        if self.icons_metadata is None:
            file = self.dir / "metadata/icons.yml"
            self.icons_metadata = safe_load(file.read_text())

        return self.icons_metadata

    def get_css(self) -> str:
        """Returns the complete path to the css file from _static folder."""
        return "../_font/fontawesome/css/all.min.css"

    def get_js(self) -> str:
        """Returns the complete path to the js file from _static folder."""
        return "../_font/fontawesome/js/all.min.js"
