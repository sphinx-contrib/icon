"""Icon extention to embed icon in sphinx outputs."""

from typing import Any, Dict

from sphinx.application import Sphinx

from .font_handler import Fontawesome
from .icon import _NODE_VISITORS, Icon, icon_node

__version__ = "0.1.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


def setup(app: Sphinx) -> Dict[str, Any]:
    """Add icon node to the sphinx builder."""
    app.add_node(icon_node, **_NODE_VISITORS)  # type: ignore
    app.add_role("icon", Icon())
    app.add_css_file(str(Fontawesome.css_file.resolve()))
    app.add_js_file(str(Fontawesome.js_file.resolve()))

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
