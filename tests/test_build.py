"""Test sphinxcontrib.icon extension."""


import pytest
from bs4 import BeautifulSoup, formatter

fmt = formatter.HTMLFormatter(indent=2, void_element_close_prefix=" /")


@pytest.mark.sphinx("epub", testroot="icon")
def test_icon_epub(app, status, warning):
    """Build a text output (unsuported)."""
    app.builder.build_all()

    assert "Unsupported output format (node skipped)" in warning.getvalue()


@pytest.mark.sphinx("latex", testroot="icon")
def test_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert "\\usepackage{fontawesome5}" in result
    assert "\\faIcon[solid]{folder}" in result


@pytest.mark.sphinx("html", testroot="icon")
def test_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    icon = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(icon, basename="folder_icon", extension=".html")
