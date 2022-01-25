from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from pathlib import Path
from shutil import rmtree
from yaml import safe_load


class Fontawesome:
    """
    Class wrapper to deal with fontawesome based icons
    """

    FONT_VERSION = "5.15.4"
    ASSET = "https://github.com/FortAwesome/Font-Awesome/releases/download/{version}/fontawesome-free-{version}-{type}.zip"
    TYPES = {"html": "web", "latex": "desktop"}

    icons_metadata = None
    dir = None

    def download_asset(self, format, path):

        type = self.TYPES[format]
        asset = self.ASSET.format(version=self.FONT_VERSION, type=type)

        self.dir = path / "fontawesome"
        self.dir.mkdir(exist_ok=True)
        rmtree(self.dir)

        # read the zip
        resp = urlopen(asset)
        zip_file = ZipFile(BytesIO(resp.read()))
        for file in zip_file.namelist():

            if not Path(file).suffix in [".css", ".js"]:
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

    def get_metadata(self):
        """read the yaml file to create a datatable of existing icons. Return the stored table if existing"""

        if self.icons_metadata is None:
            with (self.dir / "metadata/icons.yml").open("r") as f:
                self.icons_metadata = safe_load(f)

        return self.icons_metadata

    def get_css(self):
        """returns the complete path to the css file from _static folder"""

        return "../_font/fontawesome/css/all.min.css"

    def get_js(self):
        """returns the complete path to the js file from _static folder"""

        return "../_font/fontawesome/js/all.min.js"
