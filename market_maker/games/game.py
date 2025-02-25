from abc import ABC, abstractmethod
from typing import Dict, List, Any

class Game(ABC):
    def __init__(self):
        self.current_odds: Dict[str, float] = {}
        self.min_bet: float = 1.0
        self.max_bet: float = 1000.0
        self.player_balance: float = 0
        self.active_bets: Dict[str, float] = {}  # Track bets for each outcome

    @abstractmethod
    def initialize_game(self) -> None:
        """Initialize game specific parameters"""
        pass

    @abstractmethod
    def calculate_odds(self) -> Dict[str, float]:
        """Calculate odds for all possible outcomes"""
        pass

    @abstractmethod
    def play_round(self) -> Dict[str, Any]:
        """Play one round of the game and return results"""
        pass

    def place_bet(self, outcome: str, amount: float) -> bool:
        """
        Place a bet on a specific outcome
        Returns True if bet is valid and placed successfully
        """
        if amount < self.min_bet or amount > self.max_bet:
            return False
        if amount > self.player_balance:
            return False
        if outcome not in self.current_odds:
            return False
        
        self.player_balance -= amount
        self.active_bets[outcome] = amount
        return True

    def set_balance(self, balance: float) -> None:
        """Set player's initial balance"""
        self.player_balance = balance

    def clear_bets(self) -> None:
        """Clear all active bets after a round"""
        self.active_bets.clear() 