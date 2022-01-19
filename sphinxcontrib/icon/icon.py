# -*- coding: utf-8 -*-
from yaml import safe_load
from pathlib import Path
import re

from docutils import nodes

VAR_DIR = Path(__file__).parents[2] / "var"
METADATA_FILE = VAR_DIR / "desktop/metadata/icons.yml"
CSS_FILE = VAR_DIR / "web/css/all.min.css"
JS_FILE = VAR_DIR / "web/js/all.min.css"
OTF_FOLDER = VAR_DIR / "desktop/otf"


class icon(nodes.General, nodes.Element):
    pass


def depart_icon_node(self, node):
    """Empty depart function, everything is handled in visit"""
    pass


def visit_icon_node_html(self, node):
    """create the html output"""

    glyph = node["glyph"]
    font = node["font"]

    self.body.append(f'<i class="{font} fa-{glyph}"></i>')

    return


def visit_icon_node_latex(self, node):
    """create the latex output"""

    glyph = node["glyph"]

    # detect the font
    font_list = {"fa": None, "far": "regular", "fas": "solid", "fab": "brand"}
    font = font_list[node["font"]]

    # install fontawesome 5 package
    # TODO install it on the fly using the otf files downloaded in var
    package = "\\usepackage{fontawesome5}"
    if package not in self.elements["preamble"]:
        self.elements["preamble"] += f"{package}\n"

    # build the output
    cmd = "\\faIcon"
    if font is None:
        cmd += f"[{font}]"
    cmd += f"{{{glyph}}}"

    self.body.append(cmd)

    return


def visit_icon_node_unsuported(self, node, platform):
    """raise error when the requested output is not supported"""

    self.builder.warn(f"{platform}: unsupported output format (node skipped)")
    raise nodes.SkipNode


_NODE_VISITORS = {
    "html": (visit_icon_node_html, depart_icon_node),
    "latex": (visit_icon_node_latex, depart_icon_node),
    "man": (visit_icon_node_unsuported, None),
    "texinfo": (visit_icon_node_unsuported, None),
    "text": (visit_icon_node_unsuported, None),
}


def icon_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """add inline icons

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """

    # Read YAML file
    with METADATA_FILE.open("r") as f:
        fontawesome_icons = safe_load(f)

    # split the icon name to find the name inside
    m = re.match("^(fab|far|fa|fas) fa-(\w+)$", text)
    if not m:
        raise ValueError(f"invalid icon name: {text}")
    if not m.group(2) in fontawesome_icons:
        raise ValueError(f"icon {text} is not part of fontawesome 5.15.4")

    glyph = m.group(2)
    font = m.group(1)

    # create the node
    node = icon(glyph=glyph, font=font)

    return [node], []
