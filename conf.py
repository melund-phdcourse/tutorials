import os
import re
import sys
import subprocess
from datetime import datetime


sys.path.insert(0, os.path.abspath("exts"))

tags: set

try:
    import pygments_anyscript
except ImportError:
    raise ImportError("Please install pygments_anyscript to get AnyScript highlighting")


def tagged_commit():
    """Check if we are on a tagged commit"""
    try:
        subprocess.check_call(
            ["git", "describe", "--tags", "--exact-match", "HEAD"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return False
    else:
        return True


if tags.has("offline"):
    # offline build. e.g. for ams
    pass

if not tagged_commit() and not tags.has("offline"):
    tags.add("draft")


# `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = tags.has("draft")

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    # 3rd party extensions
    # 'sphinxcontrib.fulltoc',
    "inline_highlight",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx.ext.intersphinx",
    # 'sphinx.ext.autosectionlabel'
    "myst_parser",
    "sphinxext.opengraph",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxcontrib.youtube",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "amsmath",
    "substitution",
    "linkify",
    "html_image",
]

numfig = True

numfig_format = {
    "figure": "Fig. %s",
    "table": "Table %s",
    "code-block": "Code example %s:",
    "section": "Section %s",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]
# source_suffix = ".rst"


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

locale_dirs = ["locale/"]

gettext_compact = False


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "README.rst",
    "Thumbs.db",
    ".DS_Store",
    ".github",
    "README.md",
    "galleries/*",
]


# The name of the Pygments (syntax highlighting) style to use.
highlight_language = "AnyScriptDoc"
pygments_style = "AnyScript"

current_year = os.environ.get("YEAR", datetime.now().year)

ams_version = os.environ.get("AMS_VERSION", "7.4.3")
if not re.match("^\d\.\d\.\d", ams_version):
    raise ValueError("Wrong format for AMS version, environment variable")
ams_version_short = ams_version.rpartition(".")[0]
ams_version_x = ams_version_short + ".x"


ammr_version = os.environ.get("AMMR_VERSION", "2.4.3")
if not re.match("^\d\.\d\.\d", ammr_version):
    raise ValueError("Wrong format for AMMR version, environment variable")
ammr_version_short = ammr_version.rpartition(".")[0]

rst_epilog = f"""
.. |AMS| replace:: AnyBody Modeling System™
.. |AMS_VERSION_X| replace:: {ams_version_x}
.. |AMS_VERSION| replace:: {ams_version}
.. |AMS_VERSION_SHORT| replace:: {ams_version_short}
.. |AMMR_VERSION_SHORT| replace:: {ammr_version_short}
.. |AMMR_VERSION| replace:: {ammr_version}
.. |CURRENT_YEAR| replace:: {current_year}
.. role:: python(code)
    :language: python
"""

caution_old_tutorial = """

:::{admonition} **Old tutorial:**
:class: caution margin 
This tutorial has not yet been updated to ver. 7 of the AnyBody Modeling System. Some concepts may have changed.
:::
"""

myst_substitutions = {
    "AMS": "AnyBody Modeling System™",
    "AMS_VERSION_X": ams_version_x,
    "AMS_VERSION": ams_version_x,
    "AMS_VERSION_SHORT": ams_version_short,
    "AMMR_VERSION_SHORT": ams_version_short,
    "AMMR_VERSION": ammr_version,
    "CURRENT_YEAR": current_year,
    "caution_old_tutorial": caution_old_tutorial,
}


no_index = """
.. meta::
   :name=robots content=noindex: \ 
"""

myst_html_meta = {}


if tags.has("draft"):
    rst_epilog = rst_epilog + no_index
    myst_html_meta["robots"] = "noindex"

# General information about the project.
project = "AnyBody Tutorials"
copyright = f"{current_year}, AnyBody Technology"
author = "AnyBody Technology"

github_doc_root = "https://github.com/AnyBody/anybody-tutorial/tree/master"


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ams_version_short
# The full version, including alpha/beta/rc tags.
release = ams_version

if tags.has("draft"):
    release = release + "-dev"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#


html_title = "%s v%s" % (project, release)

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme = "redcloud"
# html_theme_options = {
#     'roottarget': index_doc,
#     'max_width': '1100px',
#     'minimal_width': '700px',
#     'borderless_decor': True,
#     'lighter_header_decor': False,
#     'sidebarwidth': "3.8in",
#     'fontcssurl': 'https://fonts.googleapis.com/css?family=Noticia+Text|Open+Sans|Droid+Sans+Mono',
#     'relbarbgcolor': '#999999',
#     'footerbgcolor': '#953337',
#     'sidebarlinkcolor': '#953337',
#     'headtextcolor': '#953337',
#     'headlinkcolor': '#953337',
# }


html_theme = "sphinx_book_theme"

pydata_html_theme_options = {
    # "external_links": [
    #     {
    #         "url": "https://anyscript.org/ammr-doc/",
    #         "name": "AMMR Documentation",
    #     },
    # ],
    "github_url": "https://github.com/anybody/anybody-tutorial/",
    # "logo": {
    #     "text": "PyData Theme",
    #     "image_dark": "logo-dark.svg",
    # },
    "use_edit_page_button": True,
    "show_toc_level": 2,
    "show_nav_level": 1,
    # "search_bar_position": "navbar",  # TODO: Deprecated - remove in future version
    # "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "navbar_start": ["navbar-logo"],
    # "navbar_center": ["navbar-nav", "navbar-version"],  # Just for testing
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # "left_sidebar_end": ["custom-template.html", "sidebar-ethical-ads.html"],
    # "footer_items": ["copyright", "sphinx-version", ""]
}

# html_sidebars = {
#     "index": [],  # Remove sidebars on landing page to save space
# }

myst_heading_anchors = 2

html_context = {
    "github_user": "anybody",
    "github_repo": "anybody-tutorial",
    "github_version": "master",
    "doc_path": ".",
}

html_theme_options = {
    # "logo_only": True,
    
    "repository_url": "https://github.com/anybody/anybody-tutorial",
    "use_repository_button": False,
    # "extra_navbar": 'Tutorials by <a href="https://anybodytech.com">AnyBody Technology</a>',
    "home_page_in_toc": False,
    "show_navbar_depth": 1,
    "use_download_button": False,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "show_navbar_depth": 2,
    "search_bar_text": "",

}


# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/AnyBodyTutorials2.svg"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

html_js_files = [
    'js/custom.js',
]


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [("custom.css", {"priority": 1000})]

html_copy_source = False

html_copy_source = False

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {'**': ['searchbox.html', 'globaltoc.html']}


pydata_html_sidebars = {
    "**": [
        "search-field",
        "back_to_manual.html",
        "sidebar-nav-bs",
        "sidebar-ethical-ads",
    ]
}

html_sidebars = {
    "**": [
        "navbar-logo.html",
        "search-field.html",
        "back_to_manual.html",
        "sbt-sidebar-nav.html",
    ]
}

if not tags.has("offline"):
    html_sidebars["**"].remove("back_to_manual.html")


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = project


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        "index",
        "AnyBodyTutorials.tex",
        "AnyBody Tutorials Documentation",
        "AnyBody Tehcnology",
        "manual",
    )
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", "anybodytutorials", "AnyBody Tutorials Documentation", [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "AnyBodyTutorials",
        "AnyBody Tutorials Documentation",
        author,
        "AnyBodyTutorials",
        "One line description of project.",
        "Miscellaneous",
    )
]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3.7", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
}

if tags.has("offline"):
    # Todo find a way to get intersphinx working for offline builds
    intersphinx_mapping["ammr"] = (
        "../../AMMR/Documentation/",
        ("../.inv/ammr.inv", "https://anyscript.org/ammr-doc/objects.inv"),
    )
else:
    if tags.has("draft"):
        intersphinx_mapping["ammr"] = ("https://anyscript.org/ammr-doc/beta/", None)
    else:
        intersphinx_mapping["ammr"] = ("https://anyscript.org/ammr-doc/", None)


# -- Options for OpenGraph Ext. ----------------------------------------------
# settings to control how the OpenGraph extension generates meta tags
ogp_site_url = "https://anyscript.org/"
ogp_site_name = "AnyScript Tutorials"
ogp_image = "https://anyscript.org/tutorials/_static/anybody_tutorials_logo.png"
ogp_use_first_image = True  # if not found defaults to 'ogp_image'


linkcheck_ignore = [
    r".*linkcheck_ignore",
    "https://doi.org/10.1115/1.4037100",  # asme.org prevents the linkcheck
    "https://doi.org/10.1115/1.4052115",  # asme.org prevents the linkcheck
    "https://dx.doi.org/10.1115/1.4001678",  # asme.org prevents the linkcheck
    "https://dx.doi.org/10.1115/1.4029258",  # asme.org prevents the linkcheck
]

linkcheck_allowed_redirects = {
    r"https://doi\.org.*": ".*",
    r"https://www\.sphinx-doc\.org/": r"https://www\.sphinx-doc\.org/en/master/",
    r"https://www\.anybodytech\.com/anybody\.html\?fwd=.*": ".*",
    r"https://www\.youtube.com/.*": "https://consent\.youtube.com/.*",
}


def setup(app):
    ...
