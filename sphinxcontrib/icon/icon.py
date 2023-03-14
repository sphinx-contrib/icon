"""The icon role definition."""

import re
from typing import List, Optional, Tuple

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
        return [icon_node(icon=self.text, location=self.get_source_info())], []


def get_glyph(text: str, location: Optional[Tuple[str, int]] = None) -> Tuple[str, str]:
    """Get the glyph from text.

    Args:
        text: The text to transform (e.g. "fas fa-folder")
        location: The file and lineos of the role

    Returns:
        (glyph, font): from the provided text. skip the node if one of them does not exist
    """
    # split the icon name to find the name inside
    m = re.match(Fontawesome.regex, text)
    if not m:
        logger.warning(f'invalid icon name: "{text}"', location=location)
        raise nodes.SkipNode
    font, glyph = m.group("font"), m.group("glyph")
    if font not in Fontawesome.html_font:
        msg = f'font "{font}" is not part of fontawesome, ignoring'
        logger.warning(msg, location=location)
        raise nodes.SkipNode
    if glyph not in Fontawesome.metadata:
        latest_glyph = Fontawesome.search_alias(glyph)
        if latest_glyph == "":
            msg = f'icon "{glyph}" is not part of fontawesome, ignoring'
            logger.warning(msg, location=location)
            raise nodes.SkipNode
        else:
            msg = f'icon "{glyph}" is an alias of "{latest_glyph}", replacing'
            logger.warning(msg, location=location)
            glyph = latest_glyph

    return font, glyph


def depart_icon_node_html(translator: SphinxTranslator, node: icon_node) -> None:
    """Depart the html node."""
    translator.body.append("</i>")
    pass


def visit_icon_node_html(translator: SphinxTranslator, node: icon_node) -> None:
    """Visit the html output."""
    location = node.get("location")  # default to None for non-regression
    font, glyph = get_glyph(node["icon"], location)
    translator.body.append(f'<i class="{Fontawesome.html_font[font]} fa-{glyph}">')

    return


def visit_icon_node_latex(translator: SphinxTranslator, node: icon_node) -> None:
    """Visit the latex output."""
    # extract info from the node
    location = node.get("location")  # default to None for non-regression
    font, glyph = get_glyph(node["icon"], location)

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
    location = node.get("location")  # default to None for non-regression
    msg = "Unsupported output format (node skipped)"
    logger.warning(msg, location=location)
    raise nodes.SkipNode


_NODE_VISITORS = {
    "html": (visit_icon_node_html, depart_icon_node_html),
    "latex": (visit_icon_node_latex, depart_icon_node_latex),
    "man": (visit_icon_node_unsuported, None),
    "texinfo": (visit_icon_node_unsuported, None),
    "text": (visit_icon_node_unsuported, None),
    "epub": (visit_icon_node_unsuported, None),
}
