<span align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/inventorium/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/inventorium/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/inventorium)](https://shields.io/badges/git-hub-last-commit)

</span>

---

# Inventorium

Illustration server for different types of APIs.

Based on the following YouTube video:

- [https://www.youtube.com/watch?v=pBASqUbZgkY](https://www.youtube.com/watch?v=pBASqUbZgkY)

This covers the following types of APIs:

- REST
- SOAP
- gRPC
- GraphQL
- Webhook
- WebSocket

## Contributing

Install the dependencies:

```shell
python -m venv .venv/
source .venv/bin/activate

pip install --editable . --group dev
pre-commit install --install-hooks
```

## Usage

Installing the project exposes an `inv` command:

```shell
inv --help
```

For example, running all the migrations:

```shell
inv migrate up 'path/to/file.db'
```
