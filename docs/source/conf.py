"""Configuration file for the Sphinx documentation builder."""

# For the full list of built-in configuration values, see the
# documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Including doctests in documentation -------------------------------
# https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#including-doctests-in-your-documentation

import os
import pathlib
import sys
from os.path import basename, dirname, realpath

import django

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
conf_py_path = '/docs/source/'  # with leading and trailing slash
html_context = {}

# -- Project information -----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'wselfedu'
copyright = '2024, Sergei Mikurov'
author = 'Sergei Mikurov'
release = '0.4.0'

# -- GitHub information ------------------------------------------------
github_user = 'svmikurov'
github_repo_name = 'wselfedu'
github_version = 'main'

# # -- Settings for Django ---------------------------------------------
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# -- General configuration ---------------------------------------------
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
    # https://sphinx-tabs.readthedocs.io/en/latest/
    'sphinx_tabs.tabs',
    # Add copy button from block
    # https://sphinx-copybutton.readthedocs.io/en/latest/#sphinx-copybutton
    'sphinx_copybutton',
    # Allow reference sections using its title
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#module-sphinx.ext.autosectionlabel
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
]

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_member_order
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []

# For extension: sphinx.ext.autosectionlabel
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#confval-autosectionlabel_prefix_document
autosectionlabel_prefix_document = True
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#confval-autosectionlabel_maxdepth
autosectionlabel_maxdepth = 2

# -- Options for HTML output -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_static_path = ['_static']

# -- Theme -------------------------------------------------------------
# html_theme = 'sphinx_rtd_theme'
# html_theme = 'alabaster'
html_theme = 'furo'

if html_theme == 'sphinx_rtd_theme':
    # To add a link at current page code on GitHup.
    html_context.update(
        {
            'display_github': True,
            'github_user': github_user,
            'github_repo': github_repo_name
            or basename(dirname(realpath(__file__))),
            'github_version': github_version,
            'conf_py_path': conf_py_path,
        }
    )

# -- Other -------------------------------------------------------------
add_module_names = False
autodoc_default_options = {
    'show-inheritance': True,
    'exclude-members':
        'DoesNotExist, '
        'MultipleObjectsReturned, '
        'setUpClass, '
        'setUpTestData, '
        'setUp '
}  # fmt: skip
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration
todo_include_todos = True
todo_link_only = True
