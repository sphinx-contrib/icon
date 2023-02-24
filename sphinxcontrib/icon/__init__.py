"""Icon extention to embed icon in sphinx outputs."""

from typing import Any, Dict

from sphinx.application import Sphinx

from sphinxcontrib.icon import font_handler, icon

__version__ = "0.1.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


def setup(app: Sphinx) -> Dict[str, Any]:
    """Add icon node to the sphinx builder."""
    app.add_node(icon.icon_node, **icon._NODE_VISITORS)  # type: ignore
    app.add_role("icon", icon.Icon())
    app.add_css_file(font_handler.get_css())
    app.add_js_file(font_handler.get_js())

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
