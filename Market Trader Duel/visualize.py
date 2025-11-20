import matplotlib.pyplot as plt
from simulation import run_simulation

def plot_results(steps=2000):
    # Run simulation
    results = run_simulation(steps)
    
    price_history = results['price_history']
    agent_a_history = results['agent_a']
    agent_b_history = results['agent_b']
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot Price
    ax1.plot(price_history, color='black', label='Market Price', linewidth=1)
    ax1.set_title('Market Price History')
    ax1.set_ylabel('Price ($)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot Portfolio Values
    ax2.plot(agent_a_history, color='blue', label='Agent A (Rule-Based)', linewidth=1.5)
    ax2.plot(agent_b_history, color='red', label='Agent B (Q-Learning)', linewidth=1.5)
    ax2.set_title('Agent Portfolio Value Comparison')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Portfolio Value ($)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add text summary
    final_a = agent_a_history[-1]
    final_b = agent_b_history[-1]
    winner = "Agent A" if final_a > final_b else "Agent B"
    
    summary_text = (
        f"Final Results:\n"
        f"Agent A: ${final_a:,.2f}\n"
        f"Agent B: ${final_b:,.2f}\n"
        f"Winner: {winner}"
    )
    
    # Place text box
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax2.text(0.02, 0.95, summary_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
            
    plt.tight_layout()
    
    #print simulation results on console
    print(summary_text)
    print("Results logged to simulation_history.csv")
    # Save
    output_file = 'profit_chart.png'
    plt.savefig(output_file)
    print(f"Chart saved to {output_file}")
    # plt.show() # Uncomment to view interactively

if __name__ == "__main__":
    plot_results()
