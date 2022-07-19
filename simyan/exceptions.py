"""
The Exceptions module.

This module provides the following classes:

- ServiceError
- AuthenticationError
- CacheError
"""
__all__ = ["ServiceError", "AuthenticationError", "CacheError"]


class ServiceError(Exception):
    """Class for any API errors."""

    pass


class AuthenticationError(ServiceError):
    """Class for any authentication errors."""

    pass


class CacheError(ServiceError):
    """Class for any database cache errors."""

    pass
