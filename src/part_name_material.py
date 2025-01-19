import os
import json

def load_materials():
    # Get the base directory (project root)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path to the dataset in the 'data' folder outside 'src'
    DATASET_PATH = os.path.join(BASE_DIR, 'data', 'datasettt.json')

    # Debug: print the path to verify
    print(f"Loading dataset from: {DATASET_PATH}")

    # Check if the file exists
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"The file {DATASET_PATH} does not exist.")

    # Load the JSON data
    with open(DATASET_PATH, 'r') as file:
        data = json.load(file)

    return data.get("materials", {})


def recommend_materials(part_name, top_n=3):
    """
    Recommend top N materials based on sustainability rating for a given part.
    """
    materials = load_materials()  # Load materials data
    suitable_materials = []

    for material, attributes in materials.items():
        recommended_parts = attributes.get('recommended_parts', [])
        if part_name in recommended_parts:
            sustainability_rating = attributes.get('sustainability_rating', 0)
            suitable_materials.append((material, sustainability_rating))

    if not suitable_materials:
        return []

    # Sort by sustainability rating in descending order
    suitable_materials.sort(key=lambda x: x[1], reverse=True)

    return suitable_materials[:top_n]

def main():
    """
    Main function to execute the material recommendation.
    """
    while True:
        part_name = input("\nEnter the part name for material recommendation (or type 'exit' to quit): ").strip()

        if part_name.lower() == 'exit':
            print("Exiting the recommendation system. Goodbye!")
            break

        recommendations = recommend_materials(part_name)

        if not recommendations:
            print(f"No materials found that are recommended for the part '{part_name}'. Please try another part.")
        else:
            print(f"\nTop {len(recommendations)} material(s) recommended for '{part_name}':")
            for idx, (material, rating) in enumerate(recommendations, start=1):
                print(f"{idx}. {material} (Sustainability Rating: {rating})")

if __name__ == "__main__":
    main()