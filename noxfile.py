"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv update, remove the .nox/xxx folder.
"""

import nox


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    session.install(".[doc]")
    b = session.posargs[0] if session.posargs else "html"
    session.run("sphinx-build", f"-b={b}", "-a", "-E", "docs", f"docs/_build/{b}")
