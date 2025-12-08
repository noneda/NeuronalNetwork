from Core.Logger import Logger

import sqlite3


class GlobalSqlite:
    _instance: bool = None
    running: bool = None

    _db: sqlite3 = None
    # Posible Cambio - Tenia sentido hasta que vi el nombre GlobalSqlite
    #_db: sqlite3.Connection = None

    def __new__(cls):
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
                #cls._instance._db = _init_db()
        return cls._instance

    #def _init_db() -> sqlite3.Connection:
    #   try:   
    #       self._db = sqlite3.connect("sqlite3.db", check_same_thread=False)
    #       self._db.row_factory = sqlite3.Row
    #       Logger.start(f"Creating Database Sqlite 3 {sqlite3.__version__}")
    #       return self._db
    #   except sqlite3.Error as e:
    #       Logger.error(f"Error to Connecting to Database with: \n{e}")

    def __init__(self):
        if self._initialized:
            return

        try:
            self._db.connect("sqlite3.db")
            # TODO: Posible Error al Crear la Base de datos...
            self._initialized = True
            self.running = True
            Logger.start(f"Creating Database Sqlite 3 {sqlite3.__version__}")
        except sqlite3.Error as e:
            Logger.error(f"Error to Connecting to Database with: \n{e}")

    @staticmethod
    def getDataBase(self):
        # return GlobalSqlite()._db
        return self.db
