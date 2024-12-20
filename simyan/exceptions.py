"""The Exceptions module.

This module provides the following classes:
- AuthenticationError
- ServiceError
"""

__all__ = ["AuthenticationError", "ServiceError"]


class ServiceError(Exception):
    """Class for any API errors."""


class AuthenticationError(ServiceError):
    """Class for any authentication errors."""
