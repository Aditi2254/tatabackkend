from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from src.material_recommender_model import recommend_material
from src.part_name_material import recommend_materials

app = Flask(__name__)
CORS(app)

try:
    with open('Alloy_Dataset.json', 'r') as f:
        alloy_data = json.load(f)
    print("Alloy data loaded successfully.")
except FileNotFoundError:
    print("Error: 'alloy_data.json' file not found.")
    alloy_data = []
except Exception as e:
    print(f"Unexpected error loading alloy data: {e}")
    alloy_data = []

class AlloySelector:
    def __init__(self, alloy_data):
        self.alloy_data = alloy_data

    def parse_range(self, range_str):
        try:
            min_val, max_val = map(float, range_str.split('-'))
            return min_val, max_val
        except ValueError as e:
            print(f"Error parsing range '{range_str}': {e}")
            return None, None

    def calculate_score(self, alloy, user_requirements):
        score = 0
        for prop, (min_val, max_val) in user_requirements.items():
            alloy_value = alloy.get(prop)
            if alloy_value is None:
                print(f"Property '{prop}' not found in alloy.")
                continue
            if min_val <= alloy_value <= max_val:
                score += 1
            else:
                print(f"Alloy '{alloy['name']}' failed for property '{prop}' with value {alloy_value}.")
        return score

    def find_best_alloy(self, user_requirements):
        best_alloy = None
        highest_score = -1
        for alloy in self.alloy_data:
            try:
                score = self.calculate_score(alloy, user_requirements)
                if score > highest_score:
                    best_alloy = alloy
                    highest_score = score
            except Exception as e:
                print(f"Error evaluating alloy '{alloy.get('name', 'Unknown')}': {e}")
        return best_alloy, highest_score

    def explain_composition(self, alloy):
        try:
            composition = alloy.get("composition", {})
            explanation = {element: f"{percentage}%" for element, percentage in composition.items()}
            return explanation
        except Exception as e:
            print(f"Error explaining composition for alloy '{alloy.get('name', 'Unknown')}': {e}")
            return {}

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/find-alloy', methods=['POST'])
def find_alloy():
    try:
        data = request.json
        if not data:
            print("No JSON data received in request.")
            return jsonify({"error": "Invalid input"}), 400

        user_requirements = {}
        for prop, range_str in data.items():
            min_val, max_val = AlloySelector(alloy_data).parse_range(range_str)
            if min_val is None or max_val is None:
                print(f"Invalid range for property '{prop}': {range_str}")
                continue
            user_requirements[prop] = (min_val, max_val)

        selector = AlloySelector(alloy_data)
        best_alloy, score = selector.find_best_alloy(user_requirements)
        if not best_alloy:
            print("No suitable alloy found for the given requirements.")
            return jsonify({"error": "No suitable alloy found"}), 404

        response = {
            "alloy": best_alloy,
            "score": score,
            "composition_explanation": selector.explain_composition(best_alloy)
        }
        print(f"Response prepared: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"Error in '/api/find-alloy' endpoint: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/available-properties', methods=['GET'])
def available_properties():
    try:
        properties = set()
        for alloy in alloy_data:
            properties.update(alloy.keys())
        response = {"available_properties": list(properties)}
        print(f"Available properties: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in '/api/available-properties' endpoint: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_input = data.get('properties', {})
    recommendations = recommend_material(user_input)
    return jsonify(recommendations.to_dict(orient='records'))

@app.route('/api/part-name', methods=['POST'])
def recommend_top_sustainable():
    data = request.json
    part_name = data.get('part_name', "")
    top_sustainable_recommendations = recommend_materials(part_name)
    return jsonify(top_sustainable_recommendations)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)