# Define a few simulated environmental states
# Scenario 1: Dry, weedy, and pests
env_dry_and_weedy = {
    'soil_moisture': 'low',
    'weed_level': 'high',
    'pest_status': 'present',
    'plant_growth': 'normal',
    'nutrient_level': 'optimal',
    'weather_forecast': 'sunny'
}

# Scenario 2: Just overgrown
env_overgrown = {
    'soil_moisture': 'optimal',
    'weed_level': 'none',
    'pest_status': 'none',
    'plant_growth': 'overgrown',
    'nutrient_level': 'optimal',
    'weather_forecast': 'sunny'
}

# Scenario 3: Dry, but rain is coming
env_dry_but_raining_soon = {
    'soil_moisture': 'low',
    'weed_level': 'none',
    'pest_status': 'none',
    'plant_growth': 'normal',
    'nutrient_level': 'optimal',
    'weather_forecast': 'rain_soon'
}

# Scenario 4: The perfect garden
env_perfect = {
    'soil_moisture': 'optimal',
    'weed_level': 'none',
    'pest_status': 'none',
    'plant_growth': 'normal',
    'nutrient_level': 'optimal',
    'weather_forecast': 'sunny'
}