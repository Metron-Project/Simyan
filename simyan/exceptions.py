"""
The Exceptions module.

This module provides the following classes:

- APIError
- AuthenticationError
- CacheError
"""


class APIError(Exception):
    """Class for any API errors."""

    pass


class AuthenticationError(APIError):
    """Class for any authentication errors."""

    pass


class CacheError(APIError):
    """Class for any database cache errors."""

    pass
