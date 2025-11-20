import time
from GardenAgent import GardenAgent
from preset_env_states import *

# --- Simulation ---
agent = GardenAgent()
scenarios = [
    env_dry_and_weedy, 
    env_overgrown, 
    env_dry_but_raining_soon, 
    env_perfect
]

print("\n===== RUNNING 4 SIMULATIONS WITH PRESET STATES =====")
for i, scenario in enumerate(scenarios):
    print(f"\n===== SCENARIO {i+1} =====")

    agent.perceive(scenario)
    
    action_plan = agent.generate_plan()
    
    print(f"\nAGENT'S PLAN (Executing step-by-step):")
    if not action_plan:
        print("  - No plan generated.")
    else:
        for action in action_plan:
            print(f"  - {action}")
            
    print(f"\n===== END OF SCENARIO {i+1} =====\n")