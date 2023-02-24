"""Handler to install the fontawesome resources in the build."""

from pathlib import Path
from typing import Dict

from yaml import safe_load

HERE = Path(__file__).parent
FA_DIR = HERE / "node_modules" / "@fortawesome" / "fontawesome-free"


def get_metadata() -> Dict[str, str]:
    """Read yaml file to create a datatable of existing icons.

    Returns:
         the stored table if existing
    """
    file = FA_DIR / "metadata" / "icons.yml"
    return safe_load(file.read_text())


def get_css() -> str:
    """Returns the complete path to the css file."""
    return str((FA_DIR / "css" / "all.min.css").resolve())


def get_js() -> str:
    """Returns the complete path to the js file."""
    return str((FA_DIR / "js" / "all.min.js").resolve())
