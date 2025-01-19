from dataset_preprocessing import load_material_data, preprocess_data
from utils import filter_materials

def recommend_material(user_input):
    df = load_material_data()
    df = preprocess_data(df)
    recommendations = filter_materials(df, user_input)
    
    return recommendations[['Material', 'Similarity', 'Recommended Parts']].head(5)

if __name__ == "__main__":
    user_input = {
        # Example user input
        "crashworthiness": 75,
        "corrosion_resistance": 40,
        "impact_resistance": 80,
    }
    recommendations = recommend_material(user_input)
    print(recommendations)
