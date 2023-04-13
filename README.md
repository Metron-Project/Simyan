# Simyan

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Hatch](https://img.shields.io/badge/Packaging-Hatch-4051b5?style=flat-square)](https://github.com/pypa/hatch)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?style=flat-square&logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/Code--Style-Black-000000?style=flat-square)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-informational?style=flat-square)](https://github.com/charliermarsh/ruff)

[![Github - Contributors](https://img.shields.io/github/contributors/Metron-Project/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Metron-Project/Simyan/graphs/contributors)
[![Github Action - Testing](https://img.shields.io/github/actions/workflow/status/Metron-Project/Simyan/testing.yaml?branch=main&logo=Github-Actions&label=Testing&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)

A [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.

## Installation

### PyPI

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Install the project from PyPI: `pip install simyan`

### Github

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Clone the repo: `git clone https://github.com/Metron-Project/Simyan`
3. Install the project: `pip install .`

## Example Usage

```python
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache

session = Comicvine(api_key="Comicvine API Key", cache=SQLiteCache())

# Search for Publisher
results = session.publisher_list(params={"filter": "name:DC Comics"})
for publisher in results:
    print(f"{publisher.publisher_id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
result = session.volume(volume_id=26266)
print(result.summary)
```

## Notes

Big thanks to [Mokkari](https://github.com/Metron-Project/mokkari) for the inspiration and template for this project.

Who or what is Simyan?

> Simyan along with his partner Mokkari, are the diminutive proprietors of the Evil Factory, an evil version of Project Cadmus created by Darkseid and his elite.
>
> More details at [Simyan (New Earth)](<https://dc.fandom.com/wiki/Simyan_(New_Earth)>)

## Socials

[![Social - Matrix](https://img.shields.io/matrix/metron-general:matrix.org?label=Metron%20General&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-general:matrix.org)
