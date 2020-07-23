import sys
from pathlib import Path


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent

    else:
        return Path(__file__).resolve().parents[1]
