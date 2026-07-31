import requests


class DiscordBot:

    def __init__(self, webhook=""):

        self.webhook = webhook

    # =====================================================

    def configure(self, webhook):

        self.webhook = webhook

    # =====================================================

    def enabled(self):

        return self.webhook != ""

    # =====================================================

    def send(self, message):

        if not self.enabled():

            return False

        try:

            response = requests.post(

                self.webhook,

                json={

                    "content": message

                },

                timeout=10

            )

            return response.status_code in [200, 204]

        except Exception as e:

            print("Discord Error:", e)

            return False

    # =====================================================

    def send_trade(self, result):

        text = f"""
🤖 **JARVIS AI SIGNAL**

Symbol: **{result['symbol']}**

Signal: **{result['signal']}**

Confidence: **{result['confidence']}%**

Grade: **{result['grade']}**

Entry: **{result['entry']}**

Stop Loss: **{result['stop_loss']}**

Take Profit: **{result['take_profit']}**

Risk Reward: **1:{result['risk_reward']}**

Trend: **{result['trend']}**

AI Score: **{result['score']}**
"""

        self.send(text)

    # =====================================================

    def send_closed_trade(

        self,

        symbol,

        profit

    ):

        emoji = "🟢"

        if profit < 0:

            emoji = "🔴"

        self.send(

            f"{emoji} {symbol} closed.\nProfit: {profit:.2f}"

        )