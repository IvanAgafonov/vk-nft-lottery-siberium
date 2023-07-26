import sqlite3


class SQLiteClient:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = self.dict_factory
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, params=None):
        if params is None:
            params = []
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.fetchall()

    def execute_insert(self, sql, params=None):
        if params is None:
            params = []

        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.lastrowid

    def execute_update(self, sql, params=None):
        if params is None:
            params = []

        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount

    def execute_delete(self, sql, params=None):
        if params is None:
            params = []

        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount

    def execute_select(self, sql, params=None):
        if params is None:
            params = []

        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def execute_select_one(self, sql, params=None):
        if params is None:
            params = []

        self.cursor.execute(sql, params)
        return self.cursor.fetchone()
