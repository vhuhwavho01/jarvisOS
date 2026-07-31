import sqlite3


class Performance:

    def __init__(self):

        self.db = sqlite3.connect(
            "jarvis_trades.db",
            check_same_thread=False
        )

        self.cursor = self.db.cursor()

    # =====================================================

    def total_profit(self):

        self.cursor.execute(

            "SELECT SUM(profit) FROM trades"

        )

        value = self.cursor.fetchone()[0]

        return round(value or 0, 2)

    # =====================================================

    def total_trades(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM trades"

        )

        return self.cursor.fetchone()[0]

    # =====================================================

    def wins(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM trades WHERE profit>0"

        )

        return self.cursor.fetchone()[0]

    # =====================================================

    def losses(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM trades WHERE profit<0"

        )

        return self.cursor.fetchone()[0]

    # =====================================================

    def breakeven(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM trades WHERE profit=0"

        )

        return self.cursor.fetchone()[0]

    # =====================================================

    def win_rate(self):

        total = self.total_trades()

        if total == 0:

            return 0

        return round(

            self.wins() * 100 / total,

            2

        )

    # =====================================================

    def average_win(self):

        self.cursor.execute(

            "SELECT AVG(profit) FROM trades WHERE profit>0"

        )

        value = self.cursor.fetchone()[0]

        return round(value or 0, 2)

    # =====================================================

    def average_loss(self):

        self.cursor.execute(

            "SELECT AVG(profit) FROM trades WHERE profit<0"

        )

        value = self.cursor.fetchone()[0]

        return round(value or 0, 2)

    # =====================================================

    def profit_factor(self):

        self.cursor.execute(

            "SELECT SUM(profit) FROM trades WHERE profit>0"

        )

        gross_profit = self.cursor.fetchone()[0] or 0

        self.cursor.execute(

            "SELECT ABS(SUM(profit)) FROM trades WHERE profit<0"

        )

        gross_loss = self.cursor.fetchone()[0] or 0

        if gross_loss == 0:

            return 0

        return round(

            gross_profit / gross_loss,

            2

        )

    # =====================================================

    def summary(self):

        return {

            "profit": self.total_profit(),

            "trades": self.total_trades(),

            "wins": self.wins(),

            "losses": self.losses(),

            "breakeven": self.breakeven(),

            "win_rate": self.win_rate(),

            "avg_win": self.average_win(),

            "avg_loss": self.average_loss(),

            "profit_factor": self.profit_factor()

        }