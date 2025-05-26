import sqlite3
from sqlite3 import Error

class DBSQLite:
    def __init__(self, fname):
        try:
            self.conn = sqlite3.connect(fname)
            self.sql_table()
        except Error as e:
            print(f"DB Connection Error: {e}")
            exit(1)

    def sql_table(self):
        try:
            cursorObj = self.conn.cursor()
            cursorObj.executescript('''
                CREATE TABLE IF NOT EXISTS chatbot (
                    uuid TEXT UNIQUE,
                    privilege TEXT,
                    amount_seller INTEGER,
                    amount_buyer INTEGER,
                    username_seller TEXT,
                    username_buyer TEXT
                );

                CREATE TABLE IF NOT EXISTS chatroom (
                    uuid TEXT,
                    msg_iter INTEGER,
                    msg_text TEXT
                );
            ''')
            self.conn.commit()
        except sqlite3.OperationalError as e:
            # You can log or print e if needed
            pass

    def sql_fetch(self, query, params=()):
        cursorObj = self.conn.cursor()
        cursorObj.execute(query, params)
        rows = cursorObj.fetchall()
        return rows

    def sql_update(self, query, entities):
        try:
            cursorObj = self.conn.cursor()
            cursorObj.execute(query, entities)
            self.conn.commit()
            return True, None
        except Exception as e:
            return False, f'Exception: {e}'

    def sql_exec(self, query, entities=()):
        try:
            cursorObj = self.conn.cursor()
            cursorObj.execute(query, entities)
            self.conn.commit()
            return True, None
        except Exception as e:
            return False, f'Exception: {e}'
