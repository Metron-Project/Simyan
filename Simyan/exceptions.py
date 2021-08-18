class APIError(Exception):
    pass


class AuthenticationError(APIError):
    pass


class CacheError(APIError):
    pass
