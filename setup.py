from pathlib import Path

from pynpm import NPMPackage
from setuptools import Command, setup
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from setuptools.command.sdist import sdist

ROOT = Path(__file__).parent


def update_package_data(distribution) -> None:
    """Update package_data to catch changes during setup."""
    build_py = distribution.get_command_obj("build_py")
    build_py.finalize_options()


def js_prerelease(command: Command, strict: bool = False) -> Command:
    """Decorator for building minified js/css prior to another command."""

    class DecoratedCommand(command):
        """Decorated command to install jsdeps first."""

        def run(self) -> None:
            """Run the command."""
            if not (ROOT / ".git").is_dir():  # sdist, nothing to do
                return command.run(self)

            self.distribution.run_command("jsdeps")
            command.run(self)
            update_package_data(self.distribution)

    return DecoratedCommand


class NPM(Command):
    """install package.json dependencies using npm."""

    def initialize_options(self):
        """Ignore initialize_options."""
        pass

    def finalize_options(self):
        """Ignore finalize_options."""
        pass

    def run(self):
        """Run the command."""
        pkg = NPMPackage(ROOT / "package.json")
        pkg.install()

        # update package data in case this created new files
        update_package_data(self.distribution)


setup(
    cmdclass={
        "build_py": js_prerelease(build_py),
        "egg_info": js_prerelease(egg_info),
        "sdist": js_prerelease(sdist, strict=True),
        "jsdeps": NPM,
    }
)
