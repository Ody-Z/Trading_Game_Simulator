from typing import Dict, Any
import random
from .game import Game

class DiceGame(Game):
    def __init__(self):
        super().__init__()
        self.num_dice = 3
        self.outcomes = {
            "sum_3": "Sum of 3 dice is 3",
            "sum_5_10": "Sum of 3 dice is 5 or 10",
            "sum_18": "Sum of 3 dice is 18"
        }
        self.initialize_game()

    def initialize_game(self) -> None:
        self.current_odds = self.calculate_odds()
        self.clear_bets()

    def calculate_odds(self) -> Dict[str, float]:
        base_house_edge = 0.05
        
        # Add randomness to house edge for each outcome
        house_edges = {
            "sum_3": base_house_edge + random.uniform(-0.02, 0.05),
            "sum_5_10": base_house_edge + random.uniform(-0.01, 0.04),
            "sum_18": base_house_edge + random.uniform(-0.02, 0.05),
        }
        
        # Probability calculations
        prob_sum_3 = 1/216  # (1,1,1)
        prob_sum_5_10 = 25/216  # Combined probability for 5 and 10
        prob_sum_18 = 1/216  # (6,6,6)

        # Add market fluctuation
        market_fluctuation = 0.10  # 10% maximum fluctuation
        
        # Convert probabilities to odds and add house edge
        odds = {
            "sum_3": (1 / prob_sum_3) * (1 + house_edges["sum_3"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "sum_5_10": (1 / prob_sum_5_10) * (1 + house_edges["sum_5_10"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "sum_18": (1 / prob_sum_18) * (1 + house_edges["sum_18"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation))
        }
        
        return odds

    def play_round(self) -> Dict[str, Any]:
        dice_rolls = [random.randint(1, 6) for _ in range(self.num_dice)]
        total = sum(dice_rolls)
        
        # Determine outcomes
        outcomes = {
            "sum_3": total == 3,
            "sum_5_10": total in [5, 10],
            "sum_18": total == 18
        }
        
        # Process winnings
        for outcome, won in outcomes.items():
            if outcome in self.active_bets:
                bet_amount = self.active_bets[outcome]
                if won:
                    # Return original bet plus winnings
                    self.player_balance += bet_amount + (bet_amount * (self.current_odds[outcome] - 1))
                # If bet lost, money is already deducted when bet was placed
        
        results = {
            "dice_rolls": dice_rolls,
            "total": total,
            "outcomes": outcomes
        }
        
        # Clear bets after round
        self.clear_bets()
        
        # Recalculate odds for next round
        self.current_odds = self.calculate_odds()
        
        return results 