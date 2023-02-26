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

    assert r"\usepackage{fontspec}" in result
    assert r"\newfontfamily{\solid}{fa-solid-900.ttf}" in result
    assert r"\newfontfamily{\regular}{fa-regular-400.ttf}" in result
    assert r"\newfontfamily{\brands}{fa-brands-400.ttf}" in result

    assert r'{\solid\symbol{"F07B}}' in result
    assert r'{\regular\symbol{"F007}}' in result
    assert r'{\brands\symbol{"F26E}}' in result


@pytest.mark.sphinx("latex", testroot="fa5-icon")
def test_fa5_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert r'{\solid\symbol{"F07B}}' in result
    assert r'{\regular\symbol{"F007}}' in result
    assert r'{\brands\symbol{"F26E}}' in result


@pytest.mark.sphinx("latex", testroot="fa4-icon")
def test_fa4_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert r'{\solid\symbol{"F07B}}' in result


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
