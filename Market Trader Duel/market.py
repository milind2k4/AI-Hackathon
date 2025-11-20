import random
import math

class Market:
    def __init__(self, initial_price=100.0, volatility=0.02):
        """
        Initializes the Market.

        Args:
            initial_price (float): The starting price of the commodity.
            volatility (float): The standard deviation for the random walk price updates.
        """
        self.price = initial_price
        self.volatility = volatility
        self.price_history = [self.price]

    def update_price(self):
        """
        Updates the market price using a simple random walk (Geometric Brownian Motion approximation).
        Price_t = Price_{t-1} * (1 + random_change)
        """
        change = random.gauss(0, self.volatility)
        self.price *= (1 + change)
        
        # Ensure price doesn't go negative or too close to zero
        if self.price < 0.01:
            self.price = 0.01
            
        self.price_history.append(self.price)
        return self.price

    def get_price(self):
        """
        Returns the current market price.
        """
        return self.price

    def calculate_cost(self, volume, is_buy):
        """
        Calculates the effective cost/revenue per unit including slippage/penalty.
        
        The penalty is applied to the price.
        - Buy: Effective Price = Price * (1 + penalty_factor * volume)
        - Sell: Effective Price = Price * (1 - penalty_factor * volume)
        
        This models the difficulty of filling large orders at the current spot price.
        
        Args:
            volume (int): The number of units to trade.
            is_buy (bool): True if buying, False if selling.
            
        Returns:
            float: The effective price per unit.
        """
        if volume <= 0:
            return self.price

        # Penalty factor: Small constant to scale the impact of volume
        # For example, 0.0001 means buying 100 units increases price by 1%
        penalty_factor = 0.0001 
        
        impact = penalty_factor * volume
        
        if is_buy:
            effective_price = self.price * (1 + impact)
        else:
            effective_price = self.price * (1 - impact)
            
        return effective_price
