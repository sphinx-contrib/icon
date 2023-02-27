"""The icon role definition."""

import re
from typing import List, Tuple

from docutils import nodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole, SphinxTranslator

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


def depart_icon_node_html(translator: SphinxTranslator, node: icon_node) -> None:
    """Depart the html node."""
    translator.body.append("</i>")
    pass


def visit_icon_node_html(translator: SphinxTranslator, node: icon_node) -> None:
    """Visit the html output."""
    font, glyph = get_glyph(node["icon"])
    translator.body.append(f'<i class="{Fontawesome.html_font[font]} fa-{glyph}">')

    return


def visit_icon_node_latex(translator: SphinxTranslator, node: icon_node) -> None:
    """Visit the latex output."""
    # extract info from the node
    font, glyph = get_glyph(node["icon"])

    # build the output
    font = Fontawesome.latex_font[font]
    unicode = Fontawesome.metadata[glyph]["unicode"]
    translator.body.append(r'{\%s\symbol{"%s}' % (font, unicode.upper()))

    return


def depart_icon_node_latex(translator: SphinxTranslator, node: icon_node) -> None:
    """Depart the html node."""
    translator.body.append(r"}")
    pass


def visit_icon_node_unsuported(translator: SphinxTranslator, node: icon_node) -> None:
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
