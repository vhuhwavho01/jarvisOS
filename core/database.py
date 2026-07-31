import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(

            "jarvis.db",

            check_same_thread=False

        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    # =====================================================

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS trades(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket INTEGER,

            symbol TEXT,

            direction TEXT,

            volume REAL,

            entry REAL,

            stop_loss REAL,

            take_profit REAL,

            close_price REAL,

            profit REAL,

            confidence INTEGER,

            grade TEXT,

            strategy TEXT,

            opened TEXT,

            closed TEXT

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS settings(

            name TEXT PRIMARY KEY,

            value TEXT

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS ai_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            score INTEGER,

            signal TEXT,

            confidence INTEGER,

            reasons TEXT,

            created TEXT

        )

        """)

        self.conn.commit()

    # =====================================================

    def execute(

        self,

        query,

        params=()

    ):

        self.cursor.execute(

            query,

            params

        )

        self.conn.commit()

    # =====================================================

    def fetchone(

        self,

        query,

        params=()

    ):

        self.cursor.execute(

            query,

            params

        )

        return self.cursor.fetchone()

    # =====================================================

    def fetchall(

        self,

        query,

        params=()

    ):

        self.cursor.execute(

            query,

            params

        )

        return self.cursor.fetchall()

    # =====================================================

    def close(self):

        self.conn.close()