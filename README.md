# controlcheck

Verify that documented cloud security controls actually hold in a live AWS environment.

Security policies say things like "all API activity is logged" or "administrative ports are never
exposed to the internet". `controlcheck` takes those controls, written as YAML, checks each one
against AWS using read-only API calls, and reports which ones hold, with evidence for every verdict.

> **Status:** early development. The design, threat model, and usage docs land as the tool takes shape.

## License

[Apache-2.0](LICENSE)
