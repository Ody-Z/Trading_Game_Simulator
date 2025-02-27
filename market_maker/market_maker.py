from typing import Tuple
import random

class MarketMaker:
    def __init__(self):
        self.current_bid = 19.0  # Starting bid price
        self.current_ask = 20.0  # Starting ask price
        self.spread = 1.0        # Minimum spread
        self.volatility = 0.3    # Price volatility
        self.position = 0        # Net position (positive = long, negative = short)
        self.max_position = float('inf')  # Increased maximum position size
        self.inventory_impact = 0.1  # How much position affects prices
        
    def get_prices(self) -> Tuple[float, float]:
        """Get current bid and ask prices"""
        return self.current_bid, self.current_ask
    
    def update_prices(self, card_sum: int) -> Tuple[float, float]:
        """Update prices based on market conditions with random fluctuation around 21"""
        # Use fixed base price of 21 instead of card sum
        base_price = 21.0
        
        # Add random market movement (30% range means ±15% from base)
        fluctuation_range = base_price * self.volatility # 30% of base price
        market_move = random.uniform(-fluctuation_range, fluctuation_range)
        base_price += market_move
        
        # Adjust for inventory position - when long (positive position), raise ask and lower bid
        # This encourages balancing the book by making selling more attractive and buying less attractive
        inventory_adjustment = self.position * self.inventory_impact
        
        # Update bid and ask while maintaining minimum spread
        self.current_bid = base_price - self.spread/2 - inventory_adjustment
        self.current_ask = base_price + self.spread/2 + inventory_adjustment
        
        # Ensure bid and ask are positive
        self.current_bid = max(0.1, self.current_bid)
        self.current_ask = max(self.current_bid + self.spread, self.current_ask)
        
        return self.current_bid, self.current_ask
    
    def place_trade(self, amount: float, is_buy: bool) -> bool:
        """Process a trade request"""
        # Check if trade would exceed max position
        if is_buy and self.position + amount > self.max_position:
            return False
        if not is_buy and self.position - amount < -self.max_position:
            return False
        
        # Update position
        if is_buy:
            self.position += amount
        else:
            self.position -= amount
        
        return True
    
    def get_position(self) -> float:
        """Get current position size"""
        return self.position 