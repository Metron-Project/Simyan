"""simyan package entry file."""
from importlib.metadata import version

__version__ = version("Simyan")
__all__ = ["__version__", "get_cache_root", "get_config_root", "get_project_root"]

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


def get_config_root() -> Path:
    """
    Create and return the path to the config for simyan.

    Returns:
        The path to the simyan config
    """
    folder = Path.home() / ".config" / "simyan"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_project_root() -> Path:
    """
    Return the project root path.

    Returns:
        The project root path
    """
    return Path(__file__).parent.parent
