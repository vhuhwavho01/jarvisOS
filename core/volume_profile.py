import numpy as np


class VolumeProfile:

    def __init__(self):

        self.lookback = 300

        self.bins = 40

    # =====================================================

    def calculate(self, df):

        candles = df.tail(self.lookback).copy()

        low = candles.Low.min()

        high = candles.High.max()

        edges = np.linspace(low, high, self.bins + 1)

        volume = np.zeros(self.bins)

        for _, row in candles.iterrows():

            price = (row.High + row.Low + row.Close) / 3

            idx = np.searchsorted(edges, price) - 1

            idx = max(0, min(idx, self.bins - 1))

            volume[idx] += row.Volume

        centers = (edges[:-1] + edges[1:]) / 2

        return centers, volume

    # =====================================================

    def poc(self, df):

        centers, volume = self.calculate(df)

        idx = np.argmax(volume)

        return {

            "price": round(float(centers[idx]), 2),

            "volume": float(volume[idx])

        }

    # =====================================================

    def value_area(self, df):

        centers, volume = self.calculate(df)

        total = volume.sum()

        target = total * 0.70

        order = np.argsort(volume)[::-1]

        selected = []

        running = 0

        for i in order:

            selected.append(i)

            running += volume[i]

            if running >= target:

                break

        prices = sorted(centers[selected])

        return {

            "vah": round(float(prices[-1]), 2),

            "val": round(float(prices[0]), 2)

        }

    # =====================================================

    def analyze(self, df):

        poc = self.poc(df)

        va = self.value_area(df)

        price = float(df.Close.iloc[-1])

        if price > va["vah"]:

            location = "ABOVE_VALUE"

        elif price < va["val"]:

            location = "BELOW_VALUE"

        else:

            location = "INSIDE_VALUE"

        return {

            "poc": poc,

            "vah": va["vah"],

            "val": va["val"],

            "location": location

        }