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
    assert r"\newfontfamily{\fasolid}{fa-solid-900.ttf}" in result
    assert r"\newfontfamily{\faregular}{fa-regular-400.ttf}" in result
    assert r"\newfontfamily{\fabrands}{fa-brands-400.ttf}" in result

    assert r'{\fasolid\symbol{"F07B}}' in result
    assert r'{\faregular\symbol{"F007}}' in result
    assert r'{\fabrands\symbol{"F26E}}' in result


@pytest.mark.sphinx("latex", testroot="fa5-icon")
def test_fa5_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    assert '"fas" is a deprecated alias of "fa-solid"' in warning.getvalue()
    assert '"far" is a deprecated alias of "fa-regular"' in warning.getvalue()
    assert '"fab" is a deprecated alias of "fa-brands"' in warning.getvalue()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert r'{\fasolid\symbol{"F07B}}' in result
    assert r'{\faregular\symbol{"F007}}' in result
    assert r'{\fabrands\symbol{"F26E}}' in result


@pytest.mark.sphinx("latex", testroot="fa4-icon")
def test_fa4_icon_latex(app, status, warning):
    """Build an icon role in Latex."""
    app.builder.build_all()

    assert '"fa" is a deprecated alias of "fa-solid"' in warning.getvalue()

    result = (app.outdir / "test-icon.tex").read_text(encoding="utf8")

    assert r'{\fasolid\symbol{"F07B}}' in result


@pytest.mark.sphinx("html", testroot="fa6-icon")
def test_fa6_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")

    pencil = html.select("i.fa-regular")[0].prettify(formatter=fmt)
    file_regression.check(pencil, basename="pencil_icon", extension=".html")

    github = html.select("i.fa-brands")[0].prettify(formatter=fmt)
    file_regression.check(github, basename="github_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa5-icon")
def test_fa5_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    assert '"fas" is a deprecated alias of "fa-solid"' in warning.getvalue()
    assert '"far" is a deprecated alias of "fa-regular"' in warning.getvalue()
    assert '"fab" is a deprecated alias of "fa-brands"' in warning.getvalue()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")

    pencil = html.select("i.fa-regular")[0].prettify(formatter=fmt)
    file_regression.check(pencil, basename="pencil_icon", extension=".html")

    github = html.select("i.fa-brands")[0].prettify(formatter=fmt)
    file_regression.check(github, basename="github_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa4-icon")
def test_fa4_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML."""
    app.builder.build_all()

    assert '"fa" is a deprecated alias of "fa-solid"' in warning.getvalue()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    folder = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(folder, basename="folder_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa6-alias-icon")
def test_fa6_alias_icon_html(app, status, warning, file_regression):
    """Build an icon role in HTML using the trash-alt alias for trash-can."""
    app.builder.build_all()

    assert 'icon "trash-alt" is an alias of "trash-can"' in warning.getvalue()

    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")

    trash = html.select("i.fa-solid")[0].prettify(formatter=fmt)
    file_regression.check(trash, basename="trash_can_icon", extension=".html")


@pytest.mark.sphinx("html", testroot="fa6-wrong-icon")
def test_fa6_wrong_icon_html(app, status, warning):
    """Build an icon role in HTML using a non existing icon."""
    app.builder.build_all()

    assert 'icon "toto" is not part of fontawesome' in warning.getvalue()
