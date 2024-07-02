# Simyan

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=Python&label=Python&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=Python&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=Python&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=Python&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json?style=flat-square)](https://rye.astral.sh)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json?style=flat-square)](https://github.com/astral-sh/ruff)

[![Github - Contributors](https://img.shields.io/github/contributors/Metron-Project/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Metron-Project/Simyan/graphs/contributors)
[![Github Action - Testing](https://img.shields.io/github/actions/workflow/status/Metron-Project/Simyan/testing.yaml?branch=main&logo=Github&label=Testing&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)

A [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.

## Installation

```bash
pip install Simyan
```

## Documentation

[Read the project documentation](https://simyan.readthedocs.io/en/latest/?badge=latest)

### Example Usage

```python
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache

session = Comicvine(api_key="Comicvine API Key", cache=SQLiteCache())

# Search for Publisher
results = session.list_publishers(params={"filter": "name:DC Comics"})
for publisher in results:
    print(f"{publisher.publisher_id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
result = session.get_volume(volume_id=26266)
print(result.summary)
```

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/Metron-Project/Simyan/issues) to submit bugs or request features.

## Notes

Big thanks to [Mokkari](https://github.com/Metron-Project/mokkari) for the inspiration and template for this project.

## Socials

[![Social - Matrix](https://img.shields.io/matrix/metron-general:matrix.org?label=Metron%20General&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-general:matrix.org)
