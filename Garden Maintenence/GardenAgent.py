from typing import Optional

class GardenAgent:
    def __init__(self, goal_state: Optional[dict[str, str]] = None) -> None:
        # Use the provided goal_state if given, otherwise fall back to defaults
        if goal_state is not None:
            self.goal_state = goal_state
        else:
            self.goal_state = {
                'soil_moisture': 'optimal',
                'weed_level': 'none',
                'pest_status': 'none',
                'plant_growth': 'normal',
                'nutrient_level': 'optimal'
            }
        
        self.current_state = {}
        print("Goal-Based Garden Agent initialized.\n")
        print(f"My goal is to achieve: \n{self.print_goal_state(self.goal_state)}\n")
    
    def print_goal_state(self, goal_state: dict[str, str]) -> str:
        return "\n".join([f"  - {key.replace('_', ' ').title()}: {value}" for key, value in goal_state.items()])

    def perceive(self, environment_sensors : dict[str, str]) -> None:
        self.current_state = environment_sensors
        print()
        print(f"Perceiving new environment state:")
        for key, value in self.current_state.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        print()


    def generate_plan(self) -> list[str]:
        print("Assessing state against goals and generating plan...")
        plan = []

        # Priority 1: Pests (Immediate threat)
        pest_status = self.current_state.get('pest_status', 'none')
        if pest_status == 'present' and self.goal_state['pest_status'] == 'none':
            plan.append("ACTION: Apply organic pesticide.")

        # Priority 2: Weeds (Preparation for other tasks)
        weed_level = self.current_state.get('weed_level', 'none')
        if weed_level in ['high', 'medium'] and self.goal_state['weed_level'] == 'none':
            plan.append("ACTION: Weed the garden beds.")

        # Priority 3: Water (High urgency)
        soil_moisture = self.current_state.get('soil_moisture', 'optimal')
        if soil_moisture == 'low':
            if self.current_state.get('weather_forecast') == 'rain_soon':
                plan.append("INFO: Soil is low, but rain is forecast. Skipping watering.")
            else:
                plan.append("ACTION: Water the garden.")

        # Priority 4: Nutrients (Maintenance, best done after weeding)
        nutrient_level = self.current_state.get('nutrient_level', 'optimal')
        if nutrient_level == 'low' and self.goal_state['nutrient_level'] == 'optimal':
            plan.append("ACTION: Apply fertilizer.")

        # Priority 5: Pruning (Maintenance)
        plant_growth = self.current_state.get('plant_growth', 'normal')
        if plant_growth == 'overgrown' and self.goal_state['plant_growth'] == 'normal':
            plan.append("ACTION: Prune overgrown plants.")


        # If all checks pass, the plan is empty.
        if not plan:
            plan.append("IDLE: All goals met. Monitoring.")
            
        return plan