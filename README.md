# Simyan

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=Python&label=Python&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=Python&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=Python&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=Python&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

[![Github - Contributors](https://img.shields.io/github/contributors/Metron-Project/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Metron-Project/Simyan/graphs/contributors)
[![Github Action - Testing](https://img.shields.io/github/actions/workflow/status/Metron-Project/Simyan/testing.yaml?branch=main&logo=Github&label=Testing&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/testing.yaml)
[![Github Action - Publishing](https://img.shields.io/github/actions/workflow/status/Metron-Project/Simyan/publishing.yaml?branch=main&logo=Github&label=Publishing&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/publishing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/stable)

A [Python](https://www.python.org/) wrapper for the [Comicvine API](https://comicvine.gamespot.com/api/).

## Installation

```console
pip install --user Simyan
```

### Example Usage

```python
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache

session = Comicvine(api_key="Comicvine API Key", cache=SQLiteCache())

# Search for Publisher
results = session.list_publishers(params={"filter": "name:DC Comics"})
for publisher in results:
    print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
result = session.get_volume(volume_id=26266)
print(result.summary)
```

## Documentation

- [Simyan](https://simyan.readthedocs.io/en/stable)
- [Comicvine API](https://comicvine.gamespot.com/api/documentation)

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/Metron-Project/Simyan/issues) to submit bugs or request features.

## Contributing

- When running a new test for the first time, set the environment variable `COMICVINE__API_KEY` to your Comicvine API key.
  The responses will be cached in the `tests/cache.sqlite` database without your key.

## Socials

[![Social - Matrix](https://img.shields.io/matrix/metron-general:matrix.org?label=Metron%20General&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-general:matrix.org)
[![Social - Matrix](https://img.shields.io/matrix/metron-devel:matrix.org?label=Metron%20Development&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-development:matrix.org)
