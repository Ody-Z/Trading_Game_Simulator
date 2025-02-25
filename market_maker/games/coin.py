from typing import Dict, Any
import random
from .game import Game

class CoinGame(Game):
    def __init__(self):
        super().__init__()
        self.num_coins = 3
        self.outcomes = {
            "all_heads": "All heads",
            "two_consecutive_heads": "2 consecutive heads",
            "alternating": "Alternating (HTH or THT)",
            "two_heads": "Exactly 2 heads",
            "two_tails": "Exactly 2 tails"
        }
        self.initialize_game()

    def initialize_game(self) -> None:
        self.current_odds = self.calculate_odds()
        self.clear_bets()

    def calculate_odds(self) -> Dict[str, float]:
        base_house_edge = 0.05
        
        # Add randomness to house edge for each outcome
        # This creates slightly different odds each time
        house_edges = {
            "all_heads": base_house_edge + random.uniform(-0.02, 0.05),
            "two_consecutive_heads": base_house_edge + random.uniform(-0.01, 0.04),
            "alternating": base_house_edge + random.uniform(-0.015, 0.045),
            "two_heads": base_house_edge + random.uniform(-0.01, 0.03),
            "two_tails": base_house_edge + random.uniform(-0.01, 0.03)
        }
        
        # Calculate probabilities
        prob_all_heads = 1/8
        prob_two_consecutive = 3/8
        prob_alternating = 2/8
        prob_two_heads = 3/8
        prob_two_tails = 3/8
        
        # Add a small random factor to each probability to simulate market fluctuation
        market_fluctuation = 0.1  # 10% maximum fluctuation
        
        odds = {
            "all_heads": (1 / prob_all_heads) * (1 + house_edges["all_heads"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "two_consecutive_heads": (1 / prob_two_consecutive) * (1 + house_edges["two_consecutive_heads"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "alternating": (1 / prob_alternating) * (1 + house_edges["alternating"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "two_heads": (1 / prob_two_heads) * (1 + house_edges["two_heads"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "two_tails": (1 / prob_two_tails) * (1 + house_edges["two_tails"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation))
        }
        
        return odds

    def play_round(self) -> Dict[str, Any]:
        flips = ['H' if random.random() > 0.5 else 'T' for _ in range(self.num_coins)]
        
        # Check all outcomes
        outcomes = {
            "all_heads": all(flip == 'H' for flip in flips),
            "two_consecutive_heads": any(flips[i:i+2] == ['H', 'H'] for i in range(len(flips)-1)),
            "alternating": ''.join(flips) in ['HTH', 'THT'],
            "two_heads": sum(flip == 'H' for flip in flips) == 2,
            "two_tails": sum(flip == 'T' for flip in flips) == 2
        }
        
        # Process winnings
        for outcome, won in outcomes.items():
            if outcome in self.active_bets and won:
                bet_amount = self.active_bets[outcome]
                self.player_balance += bet_amount * self.current_odds[outcome]
        
        results = {
            "flips": flips,
            "outcomes": outcomes
        }
        
        # Clear bets after round
        self.clear_bets()
        
        # Recalculate odds for next round
        self.current_odds = self.calculate_odds()
        
        return results 