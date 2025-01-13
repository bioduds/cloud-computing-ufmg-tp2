# app.py
from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

# Load rules from file
with open('rules.pkl', 'rb') as f:
    rules = pickle.load(f)

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Endpoint to get all rules"""
    return jsonify(rules)

@app.route('/api/rules/search', methods=['GET'])
def search_rules():
    """Endpoint to search rules based on antecedent"""
    antecedent = request.args.get('antecedent')
    if not antecedent:
        return jsonify({"error": "Antecedent parameter is required"}), 400

    antecedent_set = set(antecedent.split(","))
    matched_rules = [
        {"antecedent": list(rule[0]), "consequent": list(rule[1]), "confidence": rule[2]}
        for rule in rules if antecedent_set.issubset(rule[0])
    ]
    return jsonify(matched_rules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
