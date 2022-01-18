# -*- coding: utf-8 -*-
from yaml import safe_load
from pathlib import Path
import re

from docutils import nodes

class icon(nodes.General, nodes.Element):
    pass

def depart_icon_node(self, node):
    """Empty depart function, everything is handled in visit"""
    pass

def visit_icon_node_html(self, node):
    """create the html output"""
    icon = node["icon"]
    self.body.append(f"<i class=\"{icon}\"></i>")
    
    return
    
def visit_icon_node_latex(self, node):
    """create the latex output"""
    
    icon = node["unicode"]
    
    self.body.append("\\textbf{%s}" %(icon))
    
    return
        
def visit_icon_node_unsuported(self, node, platform):
    """raise error when the requested output is not supported"""
    
    self.builder.warn(f'{platform}: unsupported output format (node skipped)')
    raise nodes.SkipNode
    
_NODE_VISITORS = {
    'html': (visit_icon_node_html, depart_icon_node),
    'latex': (visit_icon_node_latex, depart_icon_node),
    'man': (visit_icon_node_unsuported, None),
    'texinfo': (visit_icon_node_unsuported, None),
    'text': (visit_icon_node_unsuported, None)
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
    font_file = Path(__file__).parents[1]/"_static/fontawesome-5.15.4-desktop/metadata/icons.yml"
    with open(font_file, 'r') as f:
        fontawesome_icons = safe_load(f)
    
    # split the icon name to find the name inside
    m = re.match("^(fab|far|fa|fas) fa-(\w+)$", text)
    if not m:
        raise ValueError(f"invalid icon name: {text}")
    
    if not m.group(2) in fontawesome_icons:
        raise ValueError(f"icon {text} is not part of fontawesome 5.15.4")
    
    unicode = fontawesome_icons[m.group(2)]["unicode"]
    
    node = icon(icon=text, unicode=unicode)
    return [node], []

def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.add_node(icon, **_NODE_VISITORS)
    app.add_role('icon', icon_role)
    return