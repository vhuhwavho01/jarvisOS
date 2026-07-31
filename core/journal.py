import sqlite3
from datetime import datetime


class TradeJournal:

    def __init__(self):

        self.db = sqlite3.connect(
            "jarvis_trades.db",
            check_same_thread=False
        )

        self.cursor = self.db.cursor()

        self.create_table()

    # =====================================================

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket INTEGER,

            symbol TEXT,

            direction TEXT,

            volume REAL,

            entry REAL,

            exit REAL,

            stop_loss REAL,

            take_profit REAL,

            profit REAL,

            confidence INTEGER,

            strategy TEXT,

            status TEXT,

            created TEXT

        )
        """)

        self.db.commit()

    # =====================================================

    def save_trade(

        self,

        ticket,

        symbol,

        direction,

        volume,

        entry,

        stop_loss,

        take_profit,

        confidence,

        strategy

    ):

        self.cursor.execute("""

        INSERT INTO trades(

            ticket,

            symbol,

            direction,

            volume,

            entry,

            exit,

            stop_loss,

            take_profit,

            profit,

            confidence,

            strategy,

            status,

            created

        )

        VALUES(

            ?,?,?,?,?,?,?,?,?,?,?,?,?

        )

        """,

        (

            ticket,

            symbol,

            direction,

            volume,

            entry,

            None,

            stop_loss,

            take_profit,

            0,

            confidence,

            strategy,

            "OPEN",

            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        )

        )

        self.db.commit()

    # =====================================================

    def close_trade(

        self,

        ticket,

        exit_price,

        profit

    ):

        self.cursor.execute("""

        UPDATE trades

        SET

        exit=?,

        profit=?,

        status='CLOSED'

        WHERE ticket=?

        """,

        (

            exit_price,

            profit,

            ticket

        )

        )

        self.db.commit()

    # =====================================================

    def get_trades(self):

        self.cursor.execute("""

        SELECT *

        FROM trades

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    # =====================================================

    def total_profit(self):

        self.cursor.execute("""

        SELECT SUM(profit)

        FROM trades

        """)

        value = self.cursor.fetchone()[0]

        return round(value or 0, 2)

    # =====================================================

    def total_trades(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM trades

        """)

        return self.cursor.fetchone()[0]

    # =====================================================

    def wins(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM trades

        WHERE profit > 0

        """)

        return self.cursor.fetchone()[0]

    # =====================================================

    def losses(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM trades

        WHERE profit < 0

        """)

        return self.cursor.fetchone()[0]

    # =====================================================

    def win_rate(self):

        total = self.total_trades()

        if total == 0:
            return 0

        wins = self.wins()

        return round((wins / total) * 100, 2)

    # =====================================================

    def clear(self):

        self.cursor.execute("""

        DELETE FROM trades

        """)

        self.db.commit()

    # =====================================================

    def close(self):

        self.db.close()