import time
from GardenAgent import GardenAgent
from generate_random_state import generate_random_state   

agent = GardenAgent()
    
print("\n===== RUNNING 5 SIMULATIONS WITH RANDOM STATES =====")
for i in range(5):
    print(f"\n===== SIMULATION {i+1} =====")
    
    current_environment = generate_random_state()
    
    agent.perceive(current_environment)
    
    action_plan = agent.generate_plan()
    
    print(f"\nAGENT'S PLAN (Executing step-by-step):")
    if not action_plan:
        print("  - No plan generated.")
    else:
        for action in action_plan:
            print(f"  - {action}")
            
    print(f"\n===== END OF SIMULATION {i+1} =====\n")