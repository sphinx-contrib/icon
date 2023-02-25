"""Test sphinxcontrib.icon extension."""


import pytest
from bs4 import BeautifulSoup, formatter

fmt = formatter.HTMLFormatter(indent=2, void_element_close_prefix=" /")


@pytest.mark.sphinx("epub", testroot="fa6-icon")
def test_icon_epub(app, status, warning):
    """Build a text output (unsuported)."""
    app.builder.build_all()

    assert "Unsupported output format (node skipped)" in warning.getvalue()


@pytest.mark.sphinx("latex", testroot="fa6-icon")
def test_fa6_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert "\\usepackage{fontawesome5}" in result
    assert "\\faIcon[solid]{folder}" in result
    assert "\\faIcon[regular]{user}" in result
    assert "\\faIcon[brand]{500px}" in result


@pytest.mark.sphinx("latex", testroot="fa5-icon")
def test_fa5_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert "\\usepackage{fontawesome5}" in result
    assert "\\faIcon[solid]{folder}" in result
    assert "\\faIcon[regular]{user}" in result
    assert "\\faIcon[brand]{500px}" in result


@pytest.mark.sphinx("latex", testroot="fa4-icon")
def test_fa4_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert "\\usepackage{fontawesome5}" in result
    assert "\\faIcon[solid]{folder}" in result


@pytest.mark.sphinx("html", testroot="fa6-icon")
def test_fa6_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")

    html.select("i.fa-regular")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="pencil_icon", extension=".html")

    html.select("i.fa-brands")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="github_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa5-icon")
def test_fa5_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")

    html.select("i.fa-regular")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="pencil_icon", extension=".html")

    html.select("i.fa-brands")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="github_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa4-icon")
def test_fa4_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")
