from typing import Dict, Any, List, Tuple
import random
from .game import Game
from ..market_maker import MarketMaker

class PokerGame(Game):
    def __init__(self):
        super().__init__()
        self.deck = self._create_deck()
        self.num_cards = 3
        self.market_maker = MarketMaker()
        self.outcomes = {
            "sum_under_10": "Sum of cards under 10",
            "sum_10_20": "Sum of cards between 10-20",
            "sum_over_20": "Sum of cards over 20",
            "all_same_suit": "All cards same suit",
            "all_face_cards": "All face cards"
        }
        # Track market maker trades
        self.mm_trades: List[Tuple[float, bool, float]] = []  # [(amount, is_buy, initial_price), ...]
        self.initialize_game()

    def initialize_game(self) -> None:
        self.current_odds = self.calculate_odds()
        self.clear_bets()
        self._shuffle_deck()
        # Reset market maker trades
        self.mm_trades.clear()

    def _create_deck(self) -> List[Tuple[str, str]]:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [(rank, suit) for suit in suits for rank in ranks]

    def _shuffle_deck(self) -> None:
        random.shuffle(self.deck)

    def _card_value(self, card: Tuple[str, str]) -> int:
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        return int(rank)

    def calculate_odds(self) -> Dict[str, float]:
        base_house_edge = 0.05
        
        # Add randomness to house edge for each outcome
        house_edges = {
            "sum_under_10": base_house_edge + random.uniform(-0.02, 0.04),
            "sum_10_20": base_house_edge + random.uniform(-0.015, 0.035),
            "sum_over_20": base_house_edge + random.uniform(-0.02, 0.04),
            "all_same_suit": base_house_edge + random.uniform(-0.01, 0.06),
            "all_face_cards": base_house_edge + random.uniform(-0.01, 0.06)
        }
        
        # Calculate probabilities
        # These are approximate probabilities
        prob_under_10 = 0.3
        prob_10_20 = 0.4
        prob_over_20 = 0.3
        prob_same_suit = 0.05
        prob_all_face = 0.037  # (12 face cards / 52 cards)^3
        
        # Add market fluctuation
        market_fluctuation = 0.10  # 10% maximum fluctuation for poker (more volatile)
        
        odds = {
            "sum_under_10": (1 / prob_under_10) * (1 + house_edges["sum_under_10"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "sum_10_20": (1 / prob_10_20) * (1 + house_edges["sum_10_20"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "sum_over_20": (1 / prob_over_20) * (1 + house_edges["sum_over_20"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "all_same_suit": (1 / prob_same_suit) * (1 + house_edges["all_same_suit"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation)),
            "all_face_cards": (1 / prob_all_face) * (1 + house_edges["all_face_cards"]) * (1 + random.uniform(-market_fluctuation, market_fluctuation))
        }
        
        return odds

    def place_market_trade(self, amount: float, is_buy: bool) -> bool:
        """Place a trade with the market maker"""
        if amount <= 0 or amount > self.player_balance:
            return False
            
        # Store the initial price for PnL calculation
        bid, ask = self.market_maker.get_prices()
        initial_price = ask if is_buy else bid
        
        success = self.market_maker.place_trade(amount, is_buy)
        if success:
            self.player_balance -= amount
            # Store amount, direction and initial price
            self.mm_trades.append((amount, is_buy, initial_price))
            return True
        return False

    def get_market_prices(self) -> Tuple[float, float]:
        """Get current market maker bid/ask prices"""
        return self.market_maker.get_prices()

    def play_round(self) -> Dict[str, Any]:
        # Reset deck and shuffle
        self.deck = self._create_deck()
        self._shuffle_deck()
        # Draw cards
        drawn_cards = [self.deck.pop() for _ in range(self.num_cards)]
        
        # Calculate sum of card values
        total = sum(self._card_value(card) for card in drawn_cards)
        
        # Check all outcomes
        outcomes = {
            "sum_under_10": total < 10,
            "sum_10_20": 10 <= total <= 20,
            "sum_over_20": total > 20,
            "all_same_suit": len(set(card[1] for card in drawn_cards)) == 1,
            "all_face_cards": all(card[0] in ['J', 'Q', 'K'] for card in drawn_cards)
        }
        
        # Process regular bet winnings
        for outcome, won in outcomes.items():
            if outcome in self.active_bets:
                bet_amount = self.active_bets[outcome]
                if won:
                    # Return original bet plus winnings
                    self.player_balance += bet_amount + (bet_amount * (self.current_odds[outcome] - 1))
                # If bet lost, money is already deducted when bet was placed
        
        # Process market maker trades
        bid, ask = self.market_maker.update_prices(total)
        for amount, is_buy, initial_price in self.mm_trades:
            if is_buy:  # Player bought (bet high)
                # Calculate PnL based on difference from initial price
                pnl = amount * (total - initial_price) 
                self.player_balance += amount + pnl
            else:  # Player sold (bet low)
                # Calculate PnL based on difference from initial price
                pnl = amount * (initial_price - total) 
                self.player_balance += amount + pnl
        
        results = {
            "cards": drawn_cards,
            "sum": total,
            "outcomes": outcomes,
            "market_prices": (bid, ask)
        }
        
        # Clear bets and trades after round
        self.clear_bets()
        self.mm_trades.clear()
        
        # Recalculate odds for next round
        self.current_odds = self.calculate_odds()
        
        return results 