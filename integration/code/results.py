"""Results module for Street Race Manager."""

import random

class ResultsModule:
    """Generates race outcomes and applies rewards/penalties."""

    def __init__(self, prize_amount=200):
        self.prize_amount = prize_amount
        self.race_history = []

    def generate_result(self, inv_ref, car_name):
        """Produce race result and update inventory accordingly."""
        roll = random.randint(1, 100)
        is_win = roll <= 50

        if is_win:
            inv_ref.update_cash(self.prize_amount)
            outcome = f"Win. Prize added: {self.prize_amount}."
        else:
            inv_ref.mark_car_damaged(car_name)
            outcome = "Loss. Car marked as damaged."

        result = {
            "win": is_win,
            "roll": roll,
            "message": outcome,
        }
        self.race_history.append(result)
        return result

    def list_results(self):
        """Return a copy of race history."""
        return list(self.race_history)
