class Confluence:

    def __init__(self):

        self.reset()

    # =====================================================

    def reset(self):

        self.score = 0

        self.reasons = []

    # =====================================================

    def add(

        self,

        condition,

        points,

        reason

    ):

        if condition:

            self.score += points

            self.reasons.append(reason)

    # =====================================================

    def subtract(

        self,

        condition,

        points,

        reason

    ):

        if condition:

            self.score -= points

            self.reasons.append(reason)

    # =====================================================

    def summary(self):

        confidence = min(abs(self.score), 100)

        if self.score >= 60:

            signal = "STRONG_BUY"

            grade = "A+"

        elif self.score >= 30:

            signal = "BUY"

            grade = "A"

        elif self.score <= -60:

            signal = "STRONG_SELL"

            grade = "A+"

        elif self.score <= -30:

            signal = "SELL"

            grade = "A"

        else:

            signal = "WAIT"

            grade = "C"

        return {

            "signal": signal,

            "confidence": confidence,

            "score": self.score,

            "grade": grade,

            "reasons": self.reasons

        }