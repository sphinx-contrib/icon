"""The icon role definition."""

import re
from pathlib import Path
from typing import List, Tuple

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole

from .font_handler import Fontawesome

font_handler = None
logger = logging.getLogger(__name__)


class icon_node(nodes.General, nodes.Element):
    """the icon node."""

    pass


class Icon(SphinxRole):
    """The icon sphinxrole interpreter."""

    def run(self) -> Tuple[List[nodes.Node], List[str]]:
        """Setup the role in the builder context."""
        return [icon_node(icon=self.text)], []


def download_font_assets(app: Sphinx) -> None:
    """Download the fonts from the web assets and prepare them to be used in the documentation output directory.

    Args:
        app: the current Sphinx application
    """
    # start the font_handler
    font_handler = Fontawesome()

    # create a _font folder
    output_dir = Path(app.outdir)
    font_dir = output_dir / "_font"
    font_dir.mkdir(exist_ok=True)
    app.config.html_static_path.append(str(font_dir))

    # guess what need to be installed based on the compiler
    if app.builder.format == "html":

        font_handler.download_asset("html", font_dir)
        app.add_css_file(font_handler.get_css())
        app.add_js_file(font_handler.get_js())

    elif app.builder.format == "latex":

        font_handler.download_asset("latex", font_dir)

    return


def get_glyph(text) -> Tuple[str, str]:
    """Get the glyph from text.

    Args:
        text: The text to transform (e.g. "fa fa-folder")

    Returns:
        (glyph, font): from the provided text. raise an error if one of them does not exist
    """
    # split the icon name to find the name inside
    m = re.match(r"^(fab|far|fa|fas) fa-([\w-]+)$", text)
    if not m:
        raise ValueError(f'invalid icon name: "{text}"')
    # if not m.group(2) in font_handler.get_metadata():
    #    raise ValueError(f'icon "{m.group(2)}" is not part of fontawesome 5.15.4')

    # return (font, glyph)
    return m.group(1), m.group(2)


def depart_icon_node_html(self, node: icon_node) -> None:
    """Depart the html node."""
    self.body.append("</i>")
    pass


def visit_icon_node_html(self, node: icon_node) -> None:
    """Visit the html output."""
    try:
        font, glyph = get_glyph(node["icon"])
    except ValueError as e:
        logger.warning(str(e), location=node)
        raise nodes.SkipNode

    self.body.append(f'<i class="{font} fa-{glyph}">')

    return


def visit_icon_node_latex(self, node: icon_node) -> None:
    """Visit the latex output."""
    try:
        font, glyph = get_glyph(node["icon"])
    except ValueError as e:
        logger.warning(str(e), location=node)
        raise nodes.SkipNode

    # detect the font
    font_list = {"fa": "", "far": "regular", "fas": "solid", "fab": "brand"}
    font = font_list[font]

    # install fontawesome 5 package
    # TODO install it on the fly using the otf files downloaded in var
    package = "\\usepackage{fontawesome5}"
    if package not in self.elements["preamble"]:
        self.elements["preamble"] += f"{package}\n"

    # build the output
    cmd = "\\faIcon"
    if font is not None:
        cmd += f"[{font}]"
    cmd += f"{{{glyph}}}"

    self.body.append(cmd)

    return


def visit_icon_node_unsuported(self, node: icon_node) -> None:
    """Raise error when the requested output is not supported."""
    logger.warning("Unsupported output format (node skipped)")
    raise nodes.SkipNode


_NODE_VISITORS = {
    "html": (visit_icon_node_html, depart_icon_node_html),
    "latex": (visit_icon_node_latex, None),
    "man": (visit_icon_node_unsuported, None),
    "texinfo": (visit_icon_node_unsuported, None),
    "text": (visit_icon_node_unsuported, None),
}
