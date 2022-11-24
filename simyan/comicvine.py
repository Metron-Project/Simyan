"""
The Comicvine module.

This module is **Deprecated**, use the `simyan.service` module instead
This module provides the following classes:

- ComicvineResource
- Comicvine
"""
__all__ = ["ComicvineResource", "Comicvine"]

from simyan import service


class ComicvineResource(service.ComicvineResource):
    """
    Enum class for Comicvine Resources.

    **Deprecated**, removed in v0.13.0, use the `simyan.service.ComicvineResource` class instead.
    """

    pass


class Comicvine(service.Comicvine):
    """
    Comicvine to request Comicvine API endpoints.

    **Deprecated**, removed in v0.13.0, use the `simyan.service.Comicvine` class instead.
    """

    pass
