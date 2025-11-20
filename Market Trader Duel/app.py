import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
from market import Market
from agents import RuleBasedTrader, QLearningTrader

st.set_page_config(page_title="Market Trader Duel", layout="wide")

# --- Session State Initialization ---
if 'market' not in st.session_state:
    st.session_state.market = Market(initial_price=100.0, volatility=0.02)
if 'agent_a' not in st.session_state:
    st.session_state.agent_a = RuleBasedTrader("Agent A (Rule-Based)", initial_cash=100000.0)
if 'agent_b' not in st.session_state:
    st.session_state.agent_b = QLearningTrader("Agent B (Q-Learning)", initial_cash=100000.0)
if 'history' not in st.session_state:
    st.session_state.history = {
        'price': [],
        'agent_a_val': [],
        'agent_b_val': [],
        'steps': []
    }
if 'running' not in st.session_state:
    st.session_state.running = False
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- Sidebar Controls ---
st.sidebar.title("Simulation Controls")

volatility = st.sidebar.slider("Market Volatility", 0.001, 0.10, 0.02, 0.001)
st.session_state.market.volatility = volatility

speed = st.sidebar.slider("Speed (Delay in seconds)", 0.0, 1.0, 0.1, 0.1)

col1, col2 = st.sidebar.columns(2)
if col1.button("Start"):
    st.session_state.running = True
if col2.button("Stop"):
    st.session_state.running = False

if st.sidebar.button("Reset Simulation"):
    st.session_state.market = Market(initial_price=100.0, volatility=volatility)
    st.session_state.agent_a = RuleBasedTrader("Agent A (Rule-Based)", initial_cash=100000.0)
    st.session_state.agent_b = QLearningTrader("Agent B (Q-Learning)", initial_cash=100000.0)
    st.session_state.history = {'price': [], 'agent_a_val': [], 'agent_b_val': [], 'steps': []}
    st.session_state.step_count = 0
    st.session_state.logs = []
    st.session_state.running = False
    st.rerun()

# --- Main Layout ---
st.title("Market Trader Duel: AI vs Rule-Based")

# Metrics
current_price = st.session_state.market.get_price()
val_a = st.session_state.agent_a.get_portfolio_value(current_price)
val_b = st.session_state.agent_b.get_portfolio_value(current_price)

m1, m2, m3 = st.columns(3)
m1.metric("Market Price", f"${current_price:,.2f}")
m2.metric("Agent A (SMA)", f"${val_a:,.2f}", delta=f"{val_a - 100000:,.2f}")
m3.metric("Agent B (Q-Learning)", f"${val_b:,.2f}", delta=f"{val_b - 100000:,.2f}")

# --- Simulation Step Logic ---
def step_simulation():
    market = st.session_state.market
    agent_a = st.session_state.agent_a
    agent_b = st.session_state.agent_b
    
    # 1. Update Price
    price = market.update_price()
    
    # 2. Agents Act
    # Agent A
    action_a, vol_a = agent_a.act(market.price_history)
    if action_a != 'hold':
        eff_price = market.calculate_cost(vol_a, action_a == 'buy')
        agent_a.execute_trade(action_a, eff_price, vol_a)
        st.session_state.logs.insert(0, f"Step {st.session_state.step_count}: Agent A {action_a}s {vol_a} @ ${eff_price:.2f}")

    # Agent B
    current_val_b = agent_b.get_portfolio_value(price)
    agent_b.learn(market.price_history, current_val_b)
    action_b, vol_b = agent_b.act(market.price_history, current_val_b)
    
    if action_b != 'hold':
        eff_price = market.calculate_cost(vol_b, action_b == 'buy')
        agent_b.execute_trade(action_b, eff_price, vol_b)
        st.session_state.logs.insert(0, f"Step {st.session_state.step_count}: Agent B {action_b}s {vol_b} @ ${eff_price:.2f}")

    # 3. Record History
    st.session_state.history['price'].append(price)
    st.session_state.history['agent_a_val'].append(agent_a.get_portfolio_value(price))
    st.session_state.history['agent_b_val'].append(agent_b.get_portfolio_value(price))
    st.session_state.history['steps'].append(st.session_state.step_count)
    
    st.session_state.step_count += 1
    
    # Limit history length for performance if needed, but 2000 is fine
    if len(st.session_state.logs) > 10:
        st.session_state.logs = st.session_state.logs[:10]

# Run Step if Running
if st.session_state.running:
    step_simulation()
    time.sleep(speed)
    st.rerun()

# --- Charts ---
# Convert history to DF for easier plotting
df = pd.DataFrame(st.session_state.history)

if not df.empty:
    # Price Chart
    st.subheader("Market Price History")
    st.line_chart(df.set_index('steps')['price'])

    # Portfolio Comparison
    st.subheader("Portfolio Performance")
    chart_data = df.set_index('steps')[['agent_a_val', 'agent_b_val']]
    st.line_chart(chart_data)

# --- Logs ---
st.subheader("Trade Log")
for log in st.session_state.logs:
    st.text(log)
