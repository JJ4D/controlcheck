"""Command-line entry point."""

import argparse
from collections.abc import Sequence

from controlcheck import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="controlcheck",
        description="Verify that documented cloud security controls hold in AWS.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Takes argv explicitly so tests can call it in-process."""
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
