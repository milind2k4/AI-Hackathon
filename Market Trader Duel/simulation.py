import matplotlib.pyplot as plt
from market import Market
from agents import RuleBasedTrader, QLearningTrader

def run_simulation(steps=1000):
    # Initialize Market
    market = Market(initial_price=100.0, volatility=0.02)
    
    # Initialize Agents
    agent_a = RuleBasedTrader("Agent A (Rule-Based)", initial_cash=100000.0)
    agent_b = QLearningTrader("Agent B (Q-Learning)", initial_cash=100000.0)
    
    agents = [agent_a, agent_b]
    
    # History for plotting
    price_history = []
    agent_a_history = []
    agent_b_history = []
    
    print(f"Starting simulation for {steps} steps...")
    
    for step in range(steps):
        # 1. Update Market Price
        current_price = market.update_price()
        price_history.append(current_price)
        
        # 2. Agent Actions
        # We pass the full price history to agents (or they manage their own view)
        # Market.price_history is available
        
        for agent in agents:
            # Calculate current portfolio value before action (for learning reward)
            current_val = agent.get_portfolio_value(current_price)
            
            if isinstance(agent, QLearningTrader):
                # Q-Learning Agent needs to learn from previous step's result first?
                # Actually, we learn AFTER the action is taken and new state is observed.
                # But here we are at step t. The agent acted at t-1.
                # So we should call learn() now based on the change from t-1 to t.
                agent.learn(market.price_history, current_val)
                
                action, volume = agent.act(market.price_history, current_val)
            elif isinstance(agent, RuleBasedTrader):
                action, volume = agent.act(market.price_history)
            else:
                action, volume = 'hold', 0
            
            # 3. Execute Trade
            if action != 'hold':
                # Calculate effective price (Slippage)
                is_buy = (action == 'buy')
                effective_price = market.calculate_cost(volume, is_buy)
                
                agent.execute_trade(action, effective_price, volume)
            
            # Log value
            agent.log_portfolio(current_price)
            
        agent_a_history.append(agent_a.get_portfolio_value(current_price))
        agent_b_history.append(agent_b.get_portfolio_value(current_price))

    print("Simulation complete.")
    
    # Save Log
    save_log({
        "agent_a_final": agent_a_history[-1],
        "agent_b_final": agent_b_history[-1],
        "steps": steps
    })
    
    return {
        "price_history": price_history,
        "agent_a": agent_a_history,
        "agent_b": agent_b_history,
        "agent_a_obj": agent_a,
        "agent_b_obj": agent_b
    }

def save_log(data, filename="simulation_history.csv"):
    import csv
    import os
    import datetime
    
    file_exists = os.path.isfile(filename)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    agent_a_val = data['agent_a_final']
    agent_b_val = data['agent_b_final']
    winner = "Agent A" if agent_a_val > agent_b_val else "Agent B"
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Steps", "Agent A Final Value", "Agent B Final Value", "Winner"])
        
        writer.writerow([timestamp, data['steps'], f"{agent_a_val:.2f}", f"{agent_b_val:.2f}", winner])

if __name__ == "__main__":
    results = run_simulation(steps=2000)
    
    # Simple text output
    print(f"Final Price: {results['price_history'][-1]:.2f}")
    print(f"Agent A Final Value: {results['agent_a'][-1]:.2f}")
    print(f"Agent B Final Value: {results['agent_b'][-1]:.2f}")
