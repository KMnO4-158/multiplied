# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
import toml
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "..")))
print(sys.path)
import multiplied as mp


# -- pyproject.toml metadata ----------------------------------------

path = Path(__file__).parents[3]
with open(path / "pyproject.toml", "r") as f:
    MP_TOML = toml.loads(f.read())

MP_VERSION = MP_TOML["project"]["version"]


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "multiplied"
copyright = "2025, Ephraim M."
author = "Ephraim M."
github = "https://github.com/EphraimCompEng/multiplied"
release = MP_VERSION
stable = "v" + ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.apidoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "jupyter_sphinx",
    "myst_parser",
]

exclude_patterns = ["multiplied.tests.rst"]
templates_path = ["_templates"]
source_suffix = [".rst", ".md"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "breeze"
html_static_path = ["_static"]
html_title = "multiplied"
html_context = {"github_user": "EphraimCompEng", "github_repo": "multiplied"}

# -- Exposing variables to .rst files ----------------------------------------
# https://stackoverflow.com/a/69211912 , https://stackoverflow.com/q/34006784
variables_to_export = [
    "project",
    "copyright",
    "release",
    "stable",
]

frozen_locals = dict(locals())

rst_epilog = "\n".join(
    map(lambda x: f".. |{x}| replace:: {frozen_locals[x]}", variables_to_export)
)
del frozen_locals
