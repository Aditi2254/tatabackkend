import math

def calculate_sustainability_score(materials_data):
    # Base weights for factors
    base_weights = {
        "carbon_footprint": 30,
        "recyclability": 25,
        "toxicity": 10,
        "energy_intensity": 15,
        "cost_effectiveness": 10,
        "supply_chain_resilience": 10,
    }

    # Factor adjustment parameter
    k = 0.1

    # Step 1: Normalize values for each factor
    def normalize(value, min_value, max_value):
        return 1 + 9 * (value - min_value) / (max_value - min_value)

    # Step 2: Calculate adjusted weights
    def adjusted_weight(base_weight, score, k):
        return base_weight * math.exp(-k * (10 - score))

    # Extract min and max values for normalization
    min_max_values = {}
    for factor in base_weights.keys():
        min_max_values[factor] = {
            "min": min(material.get(factor, 0) for material in materials_data.values()),
            "max": max(material.get(factor, 0) for material in materials_data.values()),
        }

    # Step 3: Calculate sustainability scores
    def calculate_for_material(material, factors, min_max_values):
        weighted_sum = 0
        total_weights = 0
        for factor, base_weight in factors.items():
            if factor in material:  # Ensure the factor exists in material
                normalized = normalize(
                    material[factor], 
                    min_max_values[factor]["min"], 
                    min_max_values[factor]["max"]
                )
                adj_weight = adjusted_weight(base_weight, normalized, k)
                weighted_sum += adj_weight * normalized
                total_weights += adj_weight
        return round((weighted_sum / total_weights), 2)  # Scale to 1-10

    # Calculate scores for all materials
    scores = {}
    for material_name, properties in materials_data.items():
        scores[material_name] = calculate_for_material(properties, base_weights, min_max_values)

    return scores

# Example Dataset
materials_data = {
    "Advanced High-Strength Steel (AHSS)": {
        "carbon_footprint": 80,
        "recyclability": 55,
        "toxicity": 60,
        "energy_intensity": 80,
        "cost_effectiveness": 50,
        "supply_chain_resilience": 90,
    },
    "6061 Aluminum Alloy": {
        "carbon_footprint": 60,
        "recyclability": 90,
        "toxicity": 70,
        "energy_intensity": 65,
        "cost_effectiveness": 70,
        "supply_chain_resilience": 85,
    }
}

# Calculate and print sustainability scores
sustainability_scores = calculate_sustainability_score(materials_data)
for material, score in sustainability_scores.items():
    print(f"{material}: {score}")
