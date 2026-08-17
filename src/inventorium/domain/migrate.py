import glob
import logging
import pathlib

from inventorium.domain.model import DatabaseConnection

logger = logging.getLogger(__name__)

MIGRATIONS_PATH = pathlib.Path(__file__).resolve().parent / "migrations"


def _execute_and_commit_files(
    conn: DatabaseConnection,
    files: list[str],
) -> None:
    for filepath in files:
        file = pathlib.Path(filepath)
        logger.info(f"running migration for file '{file}'")
        try:
            conn.executescript(file.read_text(encoding="utf-8"))  # type: ignore
            conn.commit()
            logger.info("successfully ran migration")
        except Exception as err:  # noqa: BLE001
            logger.error(str(err))


def migrate_up(conn: DatabaseConnection) -> None:
    up_files = sorted(
        glob.glob(str(MIGRATIONS_PATH / "*__up.sql")),
    )
    _execute_and_commit_files(conn, up_files)


def migrate_down(conn: DatabaseConnection) -> None:
    down_files = sorted(
        glob.glob(str(MIGRATIONS_PATH / "*__down.sql")),
        reverse=True,
    )
    _execute_and_commit_files(conn, down_files)
