"""The icon role definition."""

import re
from typing import List, Tuple

from docutils import nodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole

from .font_handler import Fontawesome

logger = logging.getLogger(__name__)


class icon_node(nodes.General, nodes.Element):
    """the icon node."""

    pass


class Icon(SphinxRole):
    """The icon sphinxrole interpreter."""

    def run(self) -> Tuple[List[nodes.Node], List[str]]:
        """Setup the role in the builder context."""
        return [icon_node(icon=self.text)], []


def get_glyph(text) -> Tuple[str, str]:
    """Get the glyph from text.

    Args:
        text: The text to transform (e.g. "fas fa-folder")

    Returns:
        (glyph, font): from the provided text. skip the node if one of them does not exist
    """
    # split the icon name to find the name inside
    m = re.match(Fontawesome.regex, text)
    if not m:
        logger.warning(f'invalid icon name: "{text}"')
        raise nodes.SkipNode
    if m.group("font") not in Fontawesome.html_font:
        logger.warning(f'font "{m.group("font")}" is not part of fontawesome')
        raise nodes.SkipNode
    if m.group("glyph") not in Fontawesome.metadata:
        logger.warning(f'icon "{m.group("glyph")}" is not part of fontawesome')
        raise nodes.SkipNode

    return m.group("font"), m.group("glyph")


def depart_icon_node_html(self, node: icon_node) -> None:
    """Depart the html node."""
    self.body.append("</i>")
    pass


def visit_icon_node_html(self, node: icon_node) -> None:
    """Visit the html output."""
    font, glyph = get_glyph(node["icon"])
    self.body.append(f'<i class="{Fontawesome.html_font[font]} fa-{glyph}">')

    return


def visit_icon_node_latex(self, node: icon_node) -> None:
    """Visit the latex output."""
    font, glyph = get_glyph(node["icon"])

    # detect the font
    font = Fontawesome.latex_font[font]

    # install fontawesome 5 package
    package = "\\usepackage{fontawesome5}"
    if package not in self.elements["preamble"]:
        self.elements["preamble"] += f"{package}\n"

    # build the output
    font_mark = f"[{font}]" if font else ""
    self.body.append(f"\\faIcon{font_mark}{{{glyph}}}")

    return


def depart_icon_node_latex(self, node: icon_node) -> None:
    """Everything is done in the visit method."""
    pass


def visit_icon_node_unsuported(self, node: icon_node) -> None:
    """Raise error when the requested output is not supported."""
    logger.warning("Unsupported output format (node skipped)")
    raise nodes.SkipNode


_NODE_VISITORS = {
    "html": (visit_icon_node_html, depart_icon_node_html),
    "latex": (visit_icon_node_latex, depart_icon_node_latex),
    "man": (visit_icon_node_unsuported, None),
    "texinfo": (visit_icon_node_unsuported, None),
    "text": (visit_icon_node_unsuported, None),
    "epub": (visit_icon_node_unsuported, None),
}
