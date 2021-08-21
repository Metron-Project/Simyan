# Simyan

[![Version](https://img.shields.io/github/tag-pre/Buried-In-Code/Simyan.svg?label=version&style=flat-square)](https://github.com/Buried-In-Code/Simyan/releases)
[![Issues](https://img.shields.io/github/issues/Buried-In-Code/Simyan.svg?style=flat-square)](https://github.com/Buried-In-Code/Simyan/issues)
[![Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Simyan.svg?style=flat-square)](https://github.com/Buried-In-Code/Simyan/graphs/contributors)
[![License](https://img.shields.io/github/license/Buried-In-Code/Simyan.svg?style=flat-square)](https://opensource.org/licenses/MIT)

[![Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Code-Analysis?label=Code-Analysis&logo=github&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/code-analysis.yml)

A [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.

## Built Using

- [Poetry: 1.1.7](https://python-poetry.org)
- [Python: 3.9.6](https://www.python.org/)
- [marshmallow: 3.13.0](https://pypi.org/project/marshmallow)
- [requests: 2.26.0](https://pypi.org/project/requests)
- [ratelimit: 2.2.1](https://pypi.org/project/ratelimit)

## Installation

### PyPI
```bash
$ pip install Simyan
```

## Example Usage
```python
from Simyan import api
# Your config/secrets
from config import comicvine_api_key

session = api(comicvine_api_key)

# Search for Publisher
publisher_results = session.publisher_list({'name': 'DC Comics'})
for publisher in publisher_results:
    print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

# Get details for a Volume
blackest_night = session.volume(26266)
print(blackest_night.summary)
```

*There is a cache option to limit required calls to API*
```python
from Simyan import api, SqliteCache
# Your config/secrets
from config import comicvine_api_key

session = api(comicvine_api_key, cache=SqliteCache())

# Get details for an Issue
result = session.issue(189810)
print(f"{result.volume.name} #{result.issue_number}")
print(result.description)
```

## Socials

Big thanks to [Mokkari](https://github.com/bpepple/mokkari) for the inspiration and template for this project.

[![Discord | The DEV Environment](https://discordapp.com/api/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)