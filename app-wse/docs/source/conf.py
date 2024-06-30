# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Including doctests in documentation -------------------------------------
# https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#including-doctests-in-your-documentation
import os
from os.path import basename, dirname, realpath
import pathlib
import sys
import django

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())


# -- Sey for Django ----------------------------------------------------------
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()


project = 'wselfedu'
copyright = '2024, Sergei Mikurov'
author = 'Sergei Mikurov'
release = '1.0'

github_user = "svmikurov"
github_repo_name = "wselfedu"  # auto-detected from dirname if blank
github_version = "development"
conf_py_path = "/docs/source/"   # with leading and trailing slash

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 'sphinx.ext.napoleon',
    'sphinx.ext.duration',
    # https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#including-doctests-in-your-documentation
    'sphinx.ext.doctest',
    # https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html#reusing-signatures-and-docstrings-with-autodoc
    'sphinx.ext.autodoc',
    # https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html#generating-comprehensive-api-references
    'sphinx.ext.autosummary',
    # https://myst-parser.readthedocs.io/en/v0.17.1/index.html
    'myst_parser',
]

# napoleon_google_docstring = True
# napoleon_numpy_docstring = False
# napoleon_use_ivar = False
# napoleon_use_param = True
# napoleon_type_aliases = {
#     'UserModel': 'users.models.UserModel',
#     'CategoryModel': 'english.models.CategoryModel',
#     'SourceModel': 'english.models.SourceModel',
#     'EnglishTaskSettings': 'task.settings.EnglishTaskSettings',
#     'WordLearningStories': 'english.models.word_analytic.WordLearningStories',    # noqa: E501
# }

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Add at link to page code on GitHup:
html_context = {
    "display_github": True,
    "github_user": github_user,
    "github_repo": github_repo_name or basename(dirname(realpath(__file__))),
    "github_version": github_version,
    "conf_py_path": conf_py_path,
}
