import random
import numpy as np

class Trader:
    def __init__(self, name, initial_cash=10000.0):
        self.name = name
        self.cash = initial_cash
        self.inventory = 0
        self.portfolio_history = []
        self.trade_history = [] # List of (step, action, price, volume)

    def get_portfolio_value(self, current_price):
        return self.cash + (self.inventory * current_price)

    def log_portfolio(self, current_price):
        value = self.get_portfolio_value(current_price)
        self.portfolio_history.append(value)
        return value

    def execute_trade(self, action, price, volume=1):
        """
        Executes a trade.
        Action: 'buy', 'sell', 'hold'
        Price: The effective price per unit (including slippage).
        """
        if action == 'buy':
            cost = price * volume
            self.cash -= cost
            self.inventory += volume
        elif action == 'sell':
            revenue = price * volume
            self.cash += revenue
            self.inventory -= volume
        # 'hold' does nothing

class RuleBasedTrader(Trader):
    def __init__(self, name, initial_cash=10000.0, short_window=10, long_window=50):
        super().__init__(name, initial_cash)
        self.short_window = short_window
        self.long_window = long_window

    def act(self, price_history):
        """
        Simple Moving Average Crossover Strategy.
        Buy if Short SMA > Long SMA.
        Sell if Short SMA < Long SMA.
        """
        if len(price_history) < self.long_window:
            return 'hold', 0

        short_sma = np.mean(price_history[-self.short_window:])
        long_sma = np.mean(price_history[-self.long_window:])

        # Simple logic: Always try to be Long if Bullish, Neutral/Short if Bearish
        # To avoid churning, we could add a threshold or only trade on cross.
        # For this duel, let's be aggressive:
        # If Short > Long and we don't have much inventory, Buy.
        # If Short < Long and we have inventory, Sell.
        
        # Let's define a target inventory? 
        # Or just: Buy 1 unit if Bullish, Sell 1 unit if Bearish.
        
        if short_sma > long_sma:
            return 'buy', 10 # Buy 10 units
        elif short_sma < long_sma:
            return 'sell', 10 # Sell 10 units
        
        return 'hold', 0

class QLearningTrader(Trader):
    def __init__(self, name, initial_cash=10000.0, alpha=0.1, gamma=0.9, epsilon=0.1):
        super().__init__(name, initial_cash)
        self.alpha = alpha # Learning rate
        self.gamma = gamma # Discount factor
        self.epsilon = epsilon # Exploration rate
        self.q_table = {} # Map state -> [q_buy, q_sell, q_hold]
        self.last_state = None
        self.last_action = None
        self.last_portfolio_value = initial_cash
        
        # Actions: 0=Buy, 1=Sell, 2=Hold
        self.actions = ['buy', 'sell', 'hold']

    def get_state(self, price_history):
        """
        Discretize state space:
        1. Price Trend (last 5 steps): Up, Flat, Down
        2. Inventory Level: Long, Neutral, Short (simplified)
        """
        if len(price_history) < 5:
            trend = 'flat'
        else:
            start = price_history[-5]
            end = price_history[-1]
            change = (end - start) / start
            if change > 0.01:
                trend = 'up'
            elif change < -0.01:
                trend = 'down'
            else:
                trend = 'flat'
        
        # Inventory discretization
        if self.inventory > 50:
            inv_state = 'long'
        elif self.inventory < -50:
            inv_state = 'short'
        else:
            inv_state = 'neutral'
            
        return (trend, inv_state)

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(3) # Initialize with 0
        return self.q_table[state]

    def act(self, price_history, current_portfolio_value):
        state = self.get_state(price_history)
        
        # Epsilon-greedy
        if random.random() < self.epsilon:
            action_idx = random.randint(0, 2)
        else:
            q_values = self.get_q_values(state)
            action_idx = np.argmax(q_values)
        
        action = self.actions[action_idx]
        
        # Store for learning step
        self.last_state = state
        self.last_action = action_idx
        self.last_portfolio_value = current_portfolio_value
        
        volume = 10 # Fixed volume for now
        return action, volume

    def learn(self, price_history, current_portfolio_value):
        """
        Update Q-Table based on reward.
        Reward = Change in Portfolio Value.
        """
        if self.last_state is None:
            return

        current_state = self.get_state(price_history)
        reward = current_portfolio_value - self.last_portfolio_value
        
        # Q-Learning Update Rule
        # Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s,a))
        
        old_q = self.get_q_values(self.last_state)[self.last_action]
        max_future_q = np.max(self.get_q_values(current_state))
        
        new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        
        self.q_table[self.last_state][self.last_action] = new_q
