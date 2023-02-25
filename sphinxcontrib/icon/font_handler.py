"""Handler to install the fontawesome resources in the build."""

from pathlib import Path

from yaml import safe_load

HERE = Path(__file__).parent


class Fontawesome:
    """All the parameter related to Fontawesome grouped in a singleton class."""

    fa_dir = HERE / "node_modules" / "@fortawesome" / "fontawesome-free"
    regex = "^(?P<font>fa[\\w-]*) fa-(?P<glyph>[\\w-]+)$"
    metadata = safe_load((fa_dir / "metadata" / "icons.yml").read_text())
    css_file = fa_dir / "css" / "all.min.css"
    js_file = fa_dir / "js" / "all.min.js"
    html_font = {
        "fa": "fa-solid",
        "fas": "fa-solid",
        "far": "fa-regular",
        "fab": "fa-brands",
        "fa-solid": "fa-solid",
        "fa-regular": "fa-regular",
        "fa-brands": "fa-brands",
    }
    latex_font = {
        "fa": "solid",
        "fas": "solid",
        "far": "regular",
        "fab": "brand",
        "fa-solid": "solid",
        "fa-regular": "regular",
        "fa-brands": "brand",
    }
