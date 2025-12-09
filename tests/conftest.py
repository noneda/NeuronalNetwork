import os
import sys
import sqlite3
import importlib
import shutil
from types import SimpleNamespace

import pytest


TEST_DB = os.path.join(os.path.dirname(__file__), "sqlite3_test.db")


def _init_test_db(path):
    # remove old DB
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.commit()
    conn.close()


@pytest.fixture(autouse=True)
def use_test_db(monkeypatch, tmp_path):
    """Fixture that forces Core.Database.GlobalSqlite to use a test sqlite file."""
    # initialize test db file in tests dir
    test_db_path = TEST_DB
    _init_test_db(test_db_path)

    # Ensure project `src/` is on sys.path so package imports like `Core` resolve
    project_root = os.path.dirname(os.path.dirname(__file__))
    src_path = os.path.join(project_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # monkeypatch GlobalSqlite to point to test DB
    import importlib
    importlib.invalidate_caches()
    import Core.Database as db_mod

    orig_new = db_mod.GlobalSqlite.__new__
    orig_init = db_mod.GlobalSqlite.__init__

    def fake_init(self):
        if getattr(self, "_initialized", False):
            return
        try:
            self._db = sqlite3.connect(test_db_path, check_same_thread=False)
            self._db.row_factory = sqlite3.Row
            self._initialized = True
            self.running = True
        except Exception:
            self._db = None
            self._initialized = False

    monkeypatch.setattr(db_mod.GlobalSqlite, "__init__", fake_init)

    # ensure a fresh singleton
    db_mod.GlobalSqlite._instance = None

    yield test_db_path

    # teardown: close connection and remove file
    try:
        inst = db_mod.GlobalSqlite._instance
        if inst and getattr(inst, "_db", None):
            inst._db.close()
    except Exception:
        pass
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
