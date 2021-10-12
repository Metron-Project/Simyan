# Simyan

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Simyan/graphs/contributors)

[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Code-Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)

[![Code Style - Black](https://img.shields.io/badge/Code--Style-Black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Code Style - Flake8](https://img.shields.io/badge/Code--Style-Flake8-informational.svg?style=flat-square)](https://github.com/PyCQA/flake8)

A [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.

## Installation

### PyPI

```bash
$ pip3 install -U --user simyan
```

## Example Usage

```python
from simyan import create_session
from simyan.sqlite_cache import SQLiteCache

session = create_session(api_key="ComicVine API Key", cache=SQLiteCache())

# Search for Publisher
results = session.publisher_list(params={"filter": "name:DC Comics"})
for publisher in results:
    print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
result = session.volume(_id=26266)
print(result.summary)
```

## Depreciation

This library is in Beta, changes will happen as the library settles.

The following is the methodology when changing public Methods, Fields and Classes:
- Fields will be updated/removed in next minor release.
- Methods will be marked as deprecated and updated/removed in next major release.
- Classes will be marked as deprecated and updated/removed in next major release.

## Socials

Big thanks to [Mokkari](https://github.com/bpepple/mokkari) for the inspiration and template for this project.

[![Social - Discord](https://img.shields.io/discord/618581423070117932.svg?logo=Discord&label=The-DEV-Environment&style=flat-square&colorB=7289da)](https://discord.gg/nqGMeGg)
![Social - Email](https://img.shields.io/badge/Email-BuriedInCode@tuta.io-red?style=flat-square&logo=Tutanota&logoColor=red)
[![Social - Twitter](https://img.shields.io/badge/Twitter-@BuriedInCode-blue?style=flat-square&logo=Twitter)](https://twitter.com/BuriedInCode)
