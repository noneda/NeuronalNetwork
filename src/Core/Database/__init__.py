from Core.Logger import Logger
import sqlite3


class GlobalSqlite:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._instance._db = None
            cls._instance.running = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        try:
            self._db = sqlite3.connect("sqlite3.db", check_same_thread=False)
            self._db.row_factory = sqlite3.Row
            self._initialized = True
            self.running = True
            Logger.start(f"Creating Database Sqlite 3 {sqlite3.version}")
        except sqlite3.Error as e:
            Logger.error(f"Error connecting to Database:\n{e}")

    @staticmethod
    def get_database():
        instance = GlobalSqlite()
        return instance._db
