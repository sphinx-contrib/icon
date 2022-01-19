__version__ = "0.0.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"

from . import icon


def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """

    # add the css files
    app.add_css_file(str(icon.CSS_FILE))

    # add the js files
    app.add_js_file(str(icon.JS_FILE))

    # create the node
    app.add_node(icon.icon, **icon._NODE_VISITORS)

    # create the role
    app.add_role("icon", icon.icon_role)

    return
