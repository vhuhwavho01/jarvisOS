import requests


class TelegramBot:

    def __init__(self, token="", chat_id=""):

        self.token = token

        self.chat_id = chat_id

    # =====================================================

    def configure(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id

    # =====================================================

    def enabled(self):

        return self.token != "" and self.chat_id != ""

    # =====================================================

    def send(self, message):

        if not self.enabled():

            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {

            "chat_id": self.chat_id,

            "text": message,

            "parse_mode": "HTML"

        }

        try:

            response = requests.post(

                url,

                data=payload,

                timeout=10

            )

            return response.status_code == 200

        except Exception as e:

            print("Telegram Error:", e)

            return False

    # =====================================================

    def send_trade(self, result):

        text = f"""
🤖 <b>JARVIS AI SIGNAL</b>

📈 Symbol: {result['symbol']}

🎯 Signal: <b>{result['signal']}</b>

⭐ Confidence: {result['confidence']}%

🏆 Grade: {result['grade']}

💰 Entry: {result['entry']}

🛑 Stop Loss: {result['stop_loss']}

🎯 Take Profit: {result['take_profit']}

⚖️ RR: 1:{result['risk_reward']}

📊 Trend: {result['trend']}

🧠 Score: {result['score']}
"""

        self.send(text)

    # =====================================================

    def send_position_closed(

        self,

        symbol,

        profit

    ):

        emoji = "🟢"

        if profit < 0:

            emoji = "🔴"

        self.send(

            f"{emoji} {symbol}\nProfit: {profit:.2f}"

        )