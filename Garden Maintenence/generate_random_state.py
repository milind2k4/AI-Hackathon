import random

def generate_random_state() -> dict[str, str]:
    """
    Generates a random dictionary of garden sensor readings.
    """
    state = {
        'soil_moisture': random.choice(['optimal', 'low', 'low', 'high']), # Skewed towards 'low'
        'weed_level': random.choice(['none', 'medium', 'high']),
        'pest_status': random.choice(['none', 'none', 'present']), # Skewed towards 'none'
        'plant_growth': random.choice(['normal', 'normal', 'overgrown']),
        'nutrient_level': random.choice(['optimal', 'low']),
        'weather_forecast': random.choice(['sunny', 'rain_soon'])
    }
    return state