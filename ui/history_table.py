import customtkinter as ctk

from core.journal import TradeJournal


class HistoryTable(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.journal = TradeJournal()

        headers = [

            "Ticket",

            "Symbol",

            "Side",

            "Entry",

            "Exit",

            "Profit",

            "Status"

        ]

        head = ctk.CTkFrame(self)

        head.pack(fill="x")

        for i, text in enumerate(headers):

            lbl = ctk.CTkLabel(

                head,

                text=text,

                width=110,

                font=("Segoe UI", 13, "bold")

            )

            lbl.grid(

                row=0,

                column=i,

                padx=2,

                pady=5

            )

        self.table = ctk.CTkScrollableFrame(

            self,

            height=220

        )

        self.table.pack(

            fill="both",

            expand=True

        )

        self.refresh()

    # =====================================================

    def refresh(self):

        for widget in self.table.winfo_children():

            widget.destroy()

        trades = self.journal.get_trades()

        for row, trade in enumerate(trades):

            values = [

                trade[1],   # ticket

                trade[2],   # symbol

                trade[3],   # direction

                trade[5],   # entry

                trade[6],   # exit

                trade[9],   # profit

                trade[12]   # status

            ]

            for col, value in enumerate(values):

                color = "white"

                if col == 2:

                    color = "lime" if value == "BUY" else "red"

                elif col == 5:

                    try:
                        color = "lime" if float(value) >= 0 else "red"
                    except:
                        color = "white"

                elif col == 6:

                    color = "cyan" if value == "OPEN" else "orange"

                lbl = ctk.CTkLabel(

                    self.table,

                    text=str(value),

                    width=110,

                    text_color=color

                )

                lbl.grid(

                    row=row,

                    column=col,

                    padx=2,

                    pady=2

                )

        self.after(

            5000,

            self.refresh

        )