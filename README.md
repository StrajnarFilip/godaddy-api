This project is not affiliated, associated, authorized, endorsed by, or in any way officially
connected with GoDaddy Inc., or any of its subsidiaries or its affiliates.


# godaddy-api

[![PyPI - Version](https://img.shields.io/pypi/v/godaddy-api.svg)](https://pypi.org/project/godaddy-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/godaddy-api.svg)](https://pypi.org/project/godaddy-api)

## Obtaining API key and secret

You can generate new API key and secret here:
https://developer.godaddy.com/keys

## API environmental variables

API Key, Secret and URL are passed as environmental variables.
- `GODADDY_API_KEY` for API Key
- `GODADDY_API_SECRET` for API Secret
- `GODADDY_API_URL` for API URL (`https://api.ote-godaddy.com/` and `https://api.godaddy.com/` at the time of writing)

Example:
```sh
export GODADDY_API_KEY='xxx'
export GODADDY_API_SECRET='yyy'
export GODADDY_API_URL='https://api.godaddy.com/'
```

## CLI utility

Included CLI utility allows you to easily set A record. You still need to set API environmental variables.

Example for `entire-domain.com`:
```sh
export GODADDY_API_KEY='xxx'
export GODADDY_API_SECRET='yyy'
export GODADDY_API_URL='https://api.godaddy.com/'

python -m godaddy_api "entire-domain.com" "@" "123.123.123.123"
```

Example for `subdomain.entire-domain.com`:
```sh
export GODADDY_API_KEY='xxx'
export GODADDY_API_SECRET='yyy'
export GODADDY_API_URL='https://api.godaddy.com/'

python -m godaddy_api "entire-domain.com" "subdomain" "123.123.123.123"
```

## Using GodaddyClient

You can use GodaddyClient class in your Python program.

Example:
```py
from godaddy_api.godaddy_client import GodaddyClient

client = GodaddyClient('xxx', 'yyy')
client.domains_available('entire-domain.com')
```

## Installation

```console
pip install godaddy-api
```

## License

`godaddy-api` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
