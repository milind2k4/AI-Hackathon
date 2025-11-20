# Market Trader Duel

## 1. Problem Statement

The objective is to create a trading simulation where two autonomous agents compete to maximize profit by buying and selling a single commodity.

- **Goal**: Maximize Portfolio Value (Cash + Inventory \* Current Price).
- **Constraint**: The market must simulate real-world friction (Slippage/Liquidity) to prevent unrealistic strategies like infinite buying.
- **Output**: A visual comparison of the agents' performance over time.

## 2. Solution Overview

We implemented a **Python-based discrete event simulation**.

- **Market**: A stochastic environment using a Random Walk (Geometric Brownian Motion) for price evolution. It includes a **Slippage Model** where large orders incur a penalty, simulating the consumption of liquidity in an order book.
- **Agents**: Two distinct strategies were chosen to contrast "Classical Technical Analysis" with "Reinforcement Learning".
- **Visualization**: A real-time interactive dashboard using **Streamlit** to observe the duel tick-by-tick.

## 3. Agent Strategies

### Agent A: The Rule-Based Trader (Classical)

**Strategy**: Simple Moving Average (SMA) Crossover.

- **Logic**:
  - Calculate **Short-Term SMA** (e.g., 10 steps).
  - Calculate **Long-Term SMA** (e.g., 50 steps).
  - **Buy Signal**: When Short SMA > Long SMA (Golden Cross).
  - **Sell Signal**: When Short SMA < Long SMA (Death Cross).
- **Reasoning**: This represents a standard "Trend Following" strategy used by human traders. It is robust in trending markets but suffers in choppy/sideways markets.

### Agent B: The Q-Learning Trader (AI)

**Strategy**: Tabular Q-Learning (Reinforcement Learning).

- **State Space**: A tuple of `(Price Trend, Inventory Status)`.
  - _Price Trend_: Up, Down, or Flat (based on last 5 steps).
  - _Inventory_: Long (>50 units), Short (<-50 units), or Neutral.
- **Action Space**: `[Buy, Sell, Hold]`.
- **Reward Function**: The change in Portfolio Value from step $t$ to $t+1$.
- **Learning**: Uses the Bellman Equation to update Q-values:
  $$Q(s,a) \leftarrow Q(s,a) + \alpha [R + \gamma \max Q(s',a') - Q(s,a)]$$
- **Reasoning**: This agent has no pre-programmed rules. It must _discover_ that buying low and selling high is profitable through trial and error (Exploration vs Exploitation).

## 4. Code Explanation

You can recreate this project by implementing the following files.

### `market.py` (The Environment)

Manages the global price and calculates trade costs.

- **`Market` Class**:
  - `update_price()`: Multiplies current price by $(1 + \text{Gaussian Noise})$.
  - `calculate_cost(volume, is_buy)`: The core constraint.
    - If Buying: $\text{Cost} = \text{Price} \times (1 + 0.0001 \times \text{Volume})$.
    - If Selling: $\text{Revenue} = \text{Price} \times (1 - 0.0001 \times \text{Volume})$.
    - _Why?_ This prevents the AI from buying 1 million units instantly. The more you buy, the more expensive it gets.

### `agents.py` (The Players)

Defines the logic for both agents.

- **`Trader` Base Class**: Tracks `cash`, `inventory`, and `portfolio_history`.
- **`RuleBasedTrader`**:
  - Maintains a history of prices.
  - Uses `numpy.mean()` to compute SMAs.
  - Returns 'buy' or 'sell' based on the crossover.
- **`QLearningTrader`**:
  - `q_table`: A dictionary mapping states to Q-values.
  - `get_state()`: Discretizes the continuous price history into simple categories (Up/Down).
  - `act()`: Uses **Epsilon-Greedy** policy (random action with probability $\epsilon$, best action otherwise).
  - `learn()`: Updates the Q-table based on the reward received.

### `simulation.py` (The Loop)

Orchestrates the duel.

- Initializes `Market` and both `Agents`.
- Runs a loop for `N` steps.
- In each step:
  1.  Market updates price.
  2.  Agents observe state and choose action.
  3.  Market calculates effective price (with slippage).
  4.  Agents execute trade.
  5.  Q-Agent learns from the result.
  6.  Data is logged.

### `app.py` (The Interface)

An interactive dashboard using **Streamlit**.

- Uses `st.session_state` to keep the simulation alive between UI updates.
- **Sidebar**: Allows tuning `Volatility` (how crazy the market is) and `Speed`.
- **Main Loop**: Calls the simulation logic step-by-step and updates live charts using `st.line_chart`.

## 5. How to Run

1.  **Install Dependencies**:
    ```bash
    pip install numpy matplotlib pandas streamlit plotly
    ```
2.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```
3.  **Run Headless Simulation** (for static chart):
    ```bash
    python visualize.py
    ```
