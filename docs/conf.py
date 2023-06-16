import os, sys

module_root = os.path.abspath('../')
print ('MODULEROOT: '+ module_root)

sys.path.append(module_root)

# 
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'decore Base | UI fastly'
copyright = '2023, Jean Rohark'
author = 'Jean Rohark'
release = '0.0.18'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx_copybutton', 'sphinx_favicon']

# Definiere die Dokumentationsklassen
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
   "show_toc_level": 3,
   "navbar_align": "right",
   "logo": {
        "text": "decore Base | UI fastly",
        }
}

html_static_path = ['_static']

html_css_files = [
    'styles/custom.css',
]

html_logo = "_static/logo.png"

favicons = [
    {"href": "favicon.ico"},
]