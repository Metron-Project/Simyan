# Simyan

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=PyPI&label=Python-Versions&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)
[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Simyan/graphs/contributors)
[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Code-Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)
[![Code Style - Black](https://img.shields.io/badge/Code--Style-Black-000000.svg?style=flat-square)](https://github.com/psf/black)

A [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.

## Installation

### PyPI

```bash
$ pip3 install -U --user Simyan
```

## Example Usage

```python
from Simyan import api
# Your config/secrets
from config import comicvine_api_key

session = api(api_key=comicvine_api_key)

# Search for Publisher
results = session.publisher_list(params={'filter': 'name:DC Comics'})
for publisher in results:
    print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
result = session.volume(_id=26266)
print(result.summary)
```

*There is a cache option to limit required calls to API*

```python
from Simyan import api, SqliteCache
# Your config/secrets
from config import comicvine_api_key

session = api(api_key=comicvine_api_key, cache=SqliteCache())

# Get details for an Issue
result = session.issue(_id=189810)
print(f"{result.volume.name} #{result.number}")
print(result.description)
```

## Socials

Big thanks to [Mokkari](https://github.com/bpepple/mokkari) for the inspiration and template for this project.

[![Social - Discord](https://img.shields.io/discord/618581423070117932.svg?logo=Discord&label=The-DEV-Environment&style=flat-square&colorB=7289da)](https://discord.gg/nqGMeGg)