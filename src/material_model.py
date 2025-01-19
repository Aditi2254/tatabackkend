import json

# Load the dataset from the JSON file
with open("Ecomaterial-Advisor-Backend/data/recommendation_dataset.json", "r", encoding='UTF8') as file:
    materials_data = json.load(file)


# Define thresholds for individual properties
property_thresholds = {
    "tensile_strength": 0.6,
    "impact_resistance": 0.6,
    "corrosion_resistance": 0.6,
    "recyclability": 0.6,
    "sustainability_rating": 0.6,
    "ductility": 0.6,
    "carbon_footprint": 0.6,
    "density": 0.6,
    "thermal_conductivity": 0.6,
    "hardness": 0.6,
    "youngs_modulus": 0.6,
    "crashworthiness": 0.6,
    "formability": 0.6,
    "thermal_expansion_coefficient": 0.6,
    "fatigue_resistance": 0.6,
    "oxidation_resistance": 0.6,
    "chemical_stability": 0.6,
    "uv_resistance": 0.6,
    "scratch_resistance": 0.6,
    "noise_reduction_capability": 0.6,
    "fire_resistance": 0.6,
    "cost_per_unit": 0.6,
    "thermal_insulation": 0.6,
    "durability": 0.6,
    "fracture_toughness": 0.6,
    "resistance_to_deformation": 0.6,
    "moisture_resistance": 0.6,
    "rolling_resistance": 0.6,
    "heat_resistance": 0.6,
    "elasticity": 0.6,
    "puncture_resistance": 0.6,
    "energy_absorption": 0.6,
    # Add more properties here as needed
}

# Function to calculate similarity
def find_similar_materials(input_json, dataset, overall_threshold=0.2):
    # Parse input JSON
    user_input = json.loads(input_json)
    user_properties = user_input["properties"]

    results = []

    # Iterate through the materials to calculate similarity
    for material, properties in dataset.items():
        # Filter properties to consider only numeric values
        filtered_properties = {k: v for k, v in properties.items() if isinstance(v, (int, float))}

        # Track individual property similarity scores
        property_similarities = []

        for prop, user_value in user_properties.items():
            if prop in filtered_properties:
                dataset_value = filtered_properties[prop]
                similarity = 1 - abs(dataset_value - user_value) / max(dataset_value, user_value, 1)
                property_similarities.append((prop, similarity))
            else:
                # If the property is missing, assume no similarity
                property_similarities.append((prop, 0))

        # Check if all individual similarities exceed their respective thresholds
        if all(
            similarity >= property_thresholds.get(prop, 0.6)
            for prop, similarity in property_similarities
        ):
            # Calculate overall similarity as the average of individual scores
            overall_similarity = sum(similarity for _, similarity in property_similarities) / len(property_similarities)
            results.append((material, overall_similarity))

    # Sort by overall similarity score (highest first)
    results.sort(key=lambda x: x[1], reverse=True)

    # Filter results based on overall threshold
    if not results or results[0][1] < overall_threshold:
        return [{"material": "No Material Found", "similarity_score": 0}]

    # Return top 3 most similar materials
    return [{"material": material, "similarity_score": round(score, 4)} for material, score in results[:3]]

# Example JSON input
input_data = json.dumps({
    "properties": {
        "tensile_strength": 1200,
        # "impact_resistance": 800,
        # "corrosion_resistance": 6,
        # "recyclability": 60,
        # "sustainability_rating": 9,
        "ductility": 55,
        # "carbon_footprint": 3,
        "density": 1.4,
        "thermal_conductivity": 0.2
    }
})

# Call the function with the dataset
similar_materials = find_similar_materials(input_data, materials_data)
print(similar_materials)
