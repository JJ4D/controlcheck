# controlcheck

Verify that documented cloud security controls actually hold in a live AWS environment.

Security policies say things like "all API activity is logged" or "administrative ports are never
exposed to the internet". `controlcheck` takes those controls, written as YAML, checks each one
against AWS using read-only API calls, and reports which ones hold, with evidence for every verdict.

> **Status:** early development. The design, threat model, and usage docs land as the tool takes shape.

## Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/) 0.13.5+.

```bash
uv sync                                       # create .venv from the lockfile
uv tool install pre-commit && pre-commit install   # enable local hooks
uv run pytest                                 # tests with coverage gate
uv run ruff check && uv run mypy              # lint and type-check
```

Dependencies resolve with a 7-day cooldown (`exclude-newer` in `pyproject.toml`), so
a release is never adopted in its first week.

## License

[Apache-2.0](LICENSE)
