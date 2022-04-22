"""Documentation configuration."""

from simyan import __version__

# -- Project information -----------------------------------------------------
project = "Simyan"
copyright = "2021, Brian Pepple"
author = "Brian Pepple"
release = __version__


# -- General configuration ---------------------------------------------------
templates_path = ["_templates"]
extensions = [
    # builtin modules
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # installed modules
    "sphinx_rtd_theme",
]


# -- Autodoc configuration ---------------------------------------------------
autoclass_content = "class"
autodoc_default_options = {
    "inherited-members": False,
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "dataclass_json_config,from_dict,from_json,schema,to_dict,to_json",
}
autodoc_inherit_docstrings = False
autodoc_member_order = "groupwise"
autodoc_typehints = "signature"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_ivar = True


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
