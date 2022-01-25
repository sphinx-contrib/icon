# -*- coding: utf-8 -*-
from pathlib import Path
import re

from docutils import nodes
from .font_handler import Fontawesome

# -- global variables ----------------------------------------------------------
font_handler = None
# ------------------------------------------------------------------------------


class icon(nodes.General, nodes.Element):
    pass


def download_font_assets(app):

    # start the font_handler
    font_handler = Fontawesome()

    # create a _font folder
    output_dir = Path(app.outdir)
    font_dir = output_dir / "_font"
    font_dir.mkdir(exist_ok=True)
    app.config.html_static_path.append(str(font_dir))

    # guess what need to be installed
    # based on the compiler
    if app.builder.format == "html":

        font_handler.download_asset("html", font_dir)
        app.add_css_file(font_handler.get_css())
        app.add_js_file(font_handler.get_js())

    elif app.builder.format == "latex":

        font_handler.download_asset("latex", font_dir)

    return


def get_glyph(text):
    """
    get the glyph from text

    Return a tuple of (glyph, font) from the provided text. raise an error if one of them does not exist

    :param text: The text to transform (e.g. "fa fa-folder")
    """

    # split the icon name to find the name inside
    m = re.match(r"^(fab|far|fa|fas) fa-([\w-]+)$", text)
    if not m:
        raise ValueError(f'invalid icon name: "{text}"')
    # if not m.group(2) in font_handler.get_metadata():
    #    raise ValueError(f'icon "{m.group(2)}" is not part of fontawesome 5.15.4')

    # return (font, glyph)
    return m.group(1), m.group(2)


def depart_icon_node(self, node):
    """Empty depart function, everything is handled in visit"""
    pass


def visit_icon_node_html(self, node):
    """create the html output"""

    try:
        font, glyph = get_glyph(node["icon"])
    except ValueError as e:
        self.builder.warn(str(e))
        raise nodes.SkipNode

    self.body.append(f'<i class="{font} fa-{glyph}"></i>')

    return


def visit_icon_node_latex(self, node):
    """create the latex output"""

    try:
        font, glyph = get_glyph(node["icon"])
    except ValueError as e:
        self.builder.warn(str(e))
        raise nodes.SkipNode

    # detect the font
    font_list = {"fa": None, "far": "regular", "fas": "solid", "fab": "brand"}
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


def visit_icon_node_unsuported(self, node):
    """raise error when the requested output is not supported"""

    self.builder.warn("Unsupported output format (node skipped)")
    raise nodes.SkipNode


_NODE_VISITORS = {
    "html": (visit_icon_node_html, depart_icon_node),
    "latex": (visit_icon_node_latex, depart_icon_node),
    "man": (visit_icon_node_unsuported, None),
    "texinfo": (visit_icon_node_unsuported, None),
    "text": (visit_icon_node_unsuported, None),
}


def icon_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    add inline icons

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

    # create the node
    node = icon(icon=text)

    return [node], []
