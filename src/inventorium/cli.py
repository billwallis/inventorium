from __future__ import annotations

import argparse
import logging
import pathlib
import sqlite3
from collections.abc import Sequence
from typing import assert_never

import inventorium.domain.migrate

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;240m%(asctime)s\033[0m  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

SUCCESS = 0
FAILURE = 1
HERE = pathlib.Path(__file__).resolve().parent


def _add_migrate_parser(
    top_level_subparser: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = top_level_subparser.add_parser("migrate")
    subparsers = parser.add_subparsers(dest="command__migrate")
    parser__up: argparse.ArgumentParser = subparsers.add_parser("up")
    parser__down: argparse.ArgumentParser = subparsers.add_parser("down")

    for p in (parser__up, parser__down):
        p.add_argument("database_path")

    return parser


def _migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    conn = None
    if getattr(args, "database_path", None) is not None:
        conn = sqlite3.connect(args.database_path)
        logger.info(f"using database at path '{args.database_path}'")

    match args.command__migrate:
        case None:
            parser.print_help()
            return SUCCESS
        case "up":
            assert conn is not None
            inventorium.domain.migrate.migrate_up(conn)
            return SUCCESS
        case "down":
            assert conn is not None
            inventorium.domain.migrate.migrate_down(conn)
            return SUCCESS
        case _ as unreachable:
            assert_never(unreachable)


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the command.
    """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parser__migrate = _add_migrate_parser(subparsers)

    args = parser.parse_args(argv)
    if args.command == "migrate":
        return _migrate(parser__migrate, args)

    parser.print_help()
    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
