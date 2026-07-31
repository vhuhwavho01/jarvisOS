import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import pandas as pd


class ChartWidget(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.figure = Figure(figsize=(12, 7), dpi=100)

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(

            self.figure,

            self

        )

        self.canvas.get_tk_widget().pack(

            fill="both",

            expand=True

        )

        self.clear()

    # =====================================================

    def clear(self):

        self.ax.clear()

        self.ax.set_facecolor("#111111")

        self.figure.patch.set_facecolor("#111111")

        self.ax.grid(True, alpha=0.15)

        self.ax.tick_params(colors="white")

        self.canvas.draw_idle()

    # =====================================================

    def draw_chart(self, df):

        self.clear()

        dates = mdates.date2num(df["Time"])

        width = 0.0006

        for i in range(len(df)):

            o = df.Open.iloc[i]
            h = df.High.iloc[i]
            l = df.Low.iloc[i]
            c = df.Close.iloc[i]

            color = "#00ff66" if c >= o else "#ff4444"

            self.ax.add_line(

                Line2D(

                    [dates[i], dates[i]],

                    [l, h],

                    color=color,

                    linewidth=1

                )

            )

            body = Rectangle(

                (

                    dates[i] - width / 2,

                    min(o, c)

                ),

                width,

                abs(c - o),

                facecolor=color,

                edgecolor=color

            )

            self.ax.add_patch(body)

        self.ax.xaxis.set_major_formatter(

            mdates.DateFormatter("%H:%M")

        )

        self.figure.autofmt_xdate()

        self.canvas.draw_idle()

    # =====================================================

    def draw_buy(self, price):

        x = self.ax.get_xlim()[1]

        self.ax.scatter(

            x,

            price,

            marker="^",

            s=180,

            color="lime",

            zorder=20

        )

    # =====================================================

    def draw_sell(self, price):

        x = self.ax.get_xlim()[1]

        self.ax.scatter(

            x,

            price,

            marker="v",

            s=180,

            color="red",

            zorder=20

        )

    # =====================================================

    def draw_horizontal(

        self,

        price,

        color,

        label

    ):

        self.ax.axhline(

            price,

            color=color,

            linestyle="--",

            linewidth=1

        )

        self.ax.text(

            self.ax.get_xlim()[1],

            price,

            f" {label}",

            color=color,

            fontsize=9,

            va="center"

        )

    # =====================================================

    def draw_order_block(

        self,

        high,

        low

    ):

        x0 = self.ax.get_xlim()[0]

        width = self.ax.get_xlim()[1] - x0

        rect = Rectangle(

            (x0, low),

            width,

            high - low,

            color="blue",

            alpha=0.15

        )

        self.ax.add_patch(rect)

    # =====================================================

    def draw_fvg(

        self,

        high,

        low

    ):

        x0 = self.ax.get_xlim()[0]

        width = self.ax.get_xlim()[1] - x0

        rect = Rectangle(

            (x0, low),

            width,

            high - low,

            color="gold",

            alpha=0.18

        )

        self.ax.add_patch(rect)

    # =====================================================

    def draw_liquidity(

        self,

        price

    ):

        self.ax.axhline(

            price,

            color="cyan",

            linestyle=":",

            linewidth=1.2

        )

    # =====================================================

    def refresh(self):

        self.canvas.draw_idle()