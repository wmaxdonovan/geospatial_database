import sys
from pathlib import Path


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent

    else:
        return Path(__file__).resolve().parents[1]


def exit_TEAL(database):
    if database is not None:
        database.conn.close()
    sys.stdout.write("Exiting TEAL")
    sys.exit()
