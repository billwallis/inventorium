from __future__ import annotations

import argparse
import logging
import pathlib
import sqlite3
from collections.abc import Sequence
from typing import assert_never

import inventorium.domain.migrate
import inventorium.domain.inventory
import inventorium.domain.product
import inventorium.domain.store

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;240m%(asctime)s\033[0m  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

SUCCESS = 0
FAILURE = 1
HERE = pathlib.Path(__file__).resolve().parent
assert HERE.parent.name == "src"
ROOT = HERE.parent.parent
DATABASE_PATH = ROOT / "inventory.db"


def _add_migrate_parser(
    top_level_subparser: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = top_level_subparser.add_parser("migrate")
    subparsers = parser.add_subparsers(dest="command__migrate")
    parser__up = subparsers.add_parser("up")
    parser__down = subparsers.add_parser("down")
    _, _ = parser__up, parser__down

    return parser


def _migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    conn = None
    if (db_path := getattr(args, "database_path", DATABASE_PATH)) is not None:
        conn = sqlite3.connect(db_path)
        logger.info(f"using database at path '{db_path}'")

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


def _add_inventory_parser(
    top_level_subparser: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = top_level_subparser.add_parser("inventory")
    subparsers = parser.add_subparsers(dest="command__inventory")
    parser__create: argparse.ArgumentParser = subparsers.add_parser("create")
    parser__read: argparse.ArgumentParser = subparsers.add_parser("read")
    parser__update: argparse.ArgumentParser = subparsers.add_parser("update")
    parser__delete: argparse.ArgumentParser = subparsers.add_parser("delete")

    for p in (parser__create, parser__read, parser__update, parser__delete):
        p.add_argument("--store-id", required=True)
        p.add_argument("--product-id", required=True)

    for p in (parser__create, parser__update):
        p.add_argument("--increase", type=int, default=0)
        p.add_argument("--decrease", type=int, default=0)

    return parser


def _inventory(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    logger.info(f"using database at path '{DATABASE_PATH}'")
    inventory_store = inventorium.domain.inventory.InventoryStore(conn)

    match args.command__inventory:
        case None:
            parser.print_help()
            return SUCCESS
        case "create":
            assert conn is not None
            print(
                inventory_store.create(
                    data=inventorium.domain.inventory.InventoryCreationData(
                        store_id=args.store_id,
                        product_id=args.product_id,
                        in_stock=args.increase - args.decrease,
                    )
                )
            )
            return SUCCESS
        case "read":
            assert conn is not None
            print(inventory_store.read(store_id=args.store_id, product_id=args.product_id))
            return SUCCESS
        case "update":
            assert conn is not None
            inventory = inventory_store.read(store_id=args.store_id, product_id=args.product_id)
            inventory.in_stock += args.increase - args.decrease
            print(inventory_store.update(resource=inventory))
            return SUCCESS
        case "delete":
            assert conn is not None
            print(inventory_store.delete(store_id=args.store_id, product_id=args.product_id))
            return SUCCESS
        case _ as unreachable:
            assert_never(unreachable)


def _add_store_parser(
    top_level_subparser: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = top_level_subparser.add_parser("store")
    subparsers = parser.add_subparsers(dest="command__store")
    parser__create: argparse.ArgumentParser = subparsers.add_parser("create")
    parser__read: argparse.ArgumentParser = subparsers.add_parser("read")
    parser__update: argparse.ArgumentParser = subparsers.add_parser("update")
    parser__delete: argparse.ArgumentParser = subparsers.add_parser("delete")

    for p in (parser__read, parser__update, parser__delete):
        p.add_argument("--id", required=True)

    for p in (parser__create, parser__update):
        p.add_argument("--name", required=True)

    return parser


def _store(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    logger.info(f"using database at path '{DATABASE_PATH}'")
    store_store = inventorium.domain.store.StoreStore(conn)

    match args.command__store:
        case None:
            parser.print_help()
            return SUCCESS
        case "create":
            assert conn is not None
            print(
                store_store.create(
                    data=inventorium.domain.store.StoreCreationData(
                        name=args.name,
                    )
                )
            )
            return SUCCESS
        case "read":
            assert conn is not None
            print(store_store.read(args.id))
            return SUCCESS
        case "update":
            assert conn is not None
            store = store_store.read(args.id)
            store.name = args.name
            print(store_store.update(resource=store))
            return SUCCESS
        case "delete":
            assert conn is not None
            print(store_store.delete(store_id=args.id))
            return SUCCESS
        case _ as unreachable:
            assert_never(unreachable)


def _add_product_parser(
    top_level_subparser: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = top_level_subparser.add_parser("product")
    subparsers = parser.add_subparsers(dest="command__product")
    parser__create: argparse.ArgumentParser = subparsers.add_parser("create")
    parser__read: argparse.ArgumentParser = subparsers.add_parser("read")
    parser__update: argparse.ArgumentParser = subparsers.add_parser("update")
    parser__delete: argparse.ArgumentParser = subparsers.add_parser("delete")

    for p in (parser__read, parser__update, parser__delete):
        p.add_argument("--id", required=True)

    for p in (parser__create, parser__update):
        p.add_argument("--name", required=True)

    return parser


def _product(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    logger.info(f"using database at path '{DATABASE_PATH}'")
    product_store = inventorium.domain.product.ProductStore(conn)

    match args.command__product:
        case None:
            parser.print_help()
            return SUCCESS
        case "create":
            assert conn is not None
            print(
                product_store.create(
                    data=inventorium.domain.product.ProductCreationData(
                        name=args.name,
                    )
                )
            )
            return SUCCESS
        case "read":
            assert conn is not None
            print(product_store.read(args.id))
            return SUCCESS
        case "update":
            assert conn is not None
            product = product_store.read(args.id)
            product.name = args.name
            print(product_store.update(resource=product))
            return SUCCESS
        case "delete":
            assert conn is not None
            print(product_store.delete(product_id=args.id))
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
    parser__store = _add_store_parser(subparsers)
    parser__product = _add_product_parser(subparsers)
    parser__inventory = _add_inventory_parser(subparsers)

    args = parser.parse_args(argv)
    if args.command == "migrate":
        return _migrate(parser__migrate, args)
    elif args.command == "store":
        return _store(parser__store, args)
    elif args.command == "product":
        return _product(parser__product, args)
    elif args.command == "inventory":
        return _inventory(parser__inventory, args)

    parser.print_help()
    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
