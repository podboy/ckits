# coding=utf-8

from urllib.parse import urljoin

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

from containers_kits.attribute import __author__
from containers_kits.attribute import __author_email__
from containers_kits.attribute import __description__
from containers_kits.attribute import __project__
from containers_kits.attribute import __urlhome__
from containers_kits.attribute import __version__

__urlcode__ = __urlhome__
__urldocs__ = __urlhome__
__urlbugs__ = urljoin(__urlhome__, "issues")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


class CustomInstallCommand(install):
    """Customized setuptools install command"""

    def run(self):
        install.run(self)  # Run the standard installation
        # Execute your custom code after installation


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(
        include=["containers_kits*", "images_kits*"],
        exclude=["containers_kits.unittest", "images_kits.unittest"]
    ),
    install_requires=all_requirements(),
    cmdclass={
        "install": CustomInstallCommand,
    }
)
