from typing import Tuple
import random

class MarketMaker:
    def __init__(self):
        self.current_bid = 10.0  # Starting bid price
        self.current_ask = 11.0  # Starting ask price
        self.spread = 1.0        # Minimum spread
        self.volatility = 0.2    # Price volatility
        self.position = 0        # Net position (positive = long, negative = short)
        self.max_position = 100  # Maximum position size
        self.inventory_impact = 0.1  # How much position affects prices
        
    def get_prices(self) -> Tuple[float, float]:
        """Get current bid and ask prices"""
        return self.current_bid, self.current_ask
    
    def update_prices(self, card_sum: int) -> Tuple[float, float]:
        """Update prices based on card sum and market conditions"""
        # Base price is the card sum
        base_price = float(card_sum)
        
        # Add random market movement
        market_move = random.uniform(-self.volatility, self.volatility)
        base_price += market_move
        
        # Adjust for inventory position
        inventory_adjustment = self.position * self.inventory_impact
        
        # Update bid and ask while maintaining minimum spread
        self.current_bid = base_price - self.spread/2 - inventory_adjustment
        self.current_ask = base_price + self.spread/2 - inventory_adjustment
        
        # Ensure bid and ask are positive
        self.current_bid = max(0.1, self.current_bid)
        self.current_ask = max(self.current_bid + self.spread, self.current_ask)
        
        return self.current_bid, self.current_ask
    
    def place_trade(self, amount: float, is_buy: bool) -> bool:
        """
        Place a trade with the market maker
        
        Args:
            amount: Trade amount
            is_buy: True for buy, False for sell
        
        Returns:
            bool: True if trade successful, False otherwise
        """
        if amount <= 0:
            return False
            
        # Check position limits
        new_position = self.position + (amount if is_buy else -amount)
        if abs(new_position) > self.max_position:
            return False
        
        # Update position
        self.position = new_position
        
        # Update prices based on trade
        price_impact = amount * 0.01  # 1% price impact per unit traded
        if is_buy:
            self.current_bid += price_impact
            self.current_ask += price_impact
        else:
            self.current_bid -= price_impact
            self.current_ask -= price_impact
            
        # Maintain minimum spread
        if self.current_ask - self.current_bid < self.spread:
            mid_price = (self.current_bid + self.current_ask) / 2
            self.current_bid = mid_price - self.spread/2
            self.current_ask = mid_price + self.spread/2
        
        return True
    
    def get_position(self) -> float:
        """Get current position size"""
        return self.position 