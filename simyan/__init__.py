"""simyan package entry file."""
__version__ = "0.11.0"
__all__ = ["__version__", "get_cache_root"]

from pathlib import Path


def get_cache_root() -> Path:
    """
    Create and return the path to the cache for simyan.

    Returns:
        The path to the simyan cache
    """
    folder = Path.home() / ".cache" / "simyan"
    folder.mkdir(parents=True, exist_ok=True)
    return folder
