class AIScore:

    def __init__(self):

        self.score = 0
        self.reasons = []

    # =====================================================

    def add(self, points, reason):

        self.score += points
        self.reasons.append(reason)

    # =====================================================

    def confidence(self):

        return min(100, abs(self.score))

    # =====================================================

    def signal(self):

        if self.score >= 70:
            return "BUY"

        if self.score <= -70:
            return "SELL"

        return "WAIT"

    # =====================================================

    def grade(self):

        c = self.confidence()

        if c >= 95:
            return "A+"

        if c >= 90:
            return "A"

        if c >= 80:
            return "B"

        if c >= 70:
            return "C"

        return "D"

    # =====================================================

    def summary(self):

        return {

            "score": self.score,

            "confidence": self.confidence(),

            "signal": self.signal(),

            "grade": self.grade(),

            "reasons": self.reasons

        }

    # =====================================================

    def reset(self):

        self.score = 0
        self.reasons = []