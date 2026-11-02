# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub's
[private vulnerability reporting](https://github.com/JJ4D/controlcheck/security/advisories/new).
Do not open a public issue.

You can expect an acknowledgement within 5 business days.

## What counts as a security issue

`controlcheck` is an assurance tool, so beyond the usual classes of bug, these are in scope:

- **False PASS results.** Any case where a control that does not hold is reported as passing,
  including when an API call fails or is denied. The tool is designed to fail closed.
- **Credential handling.** Any path where AWS credentials could be logged, written to a report,
  or accepted on the command line.
- **Write operations.** The tool must only ever call read-only AWS APIs. Any code path that
  could modify an AWS account is a vulnerability.
- **Unsafe input handling.** Control files are parsed as data. Any way a control file can cause
  code execution is a vulnerability.

## Supported versions

Only the latest release on `main` receives fixes.
