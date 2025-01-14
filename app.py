from flask import Flask, jsonify, request
import pickle
import os
import logging
from datetime import datetime

# Configurações do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Inicializa a aplicação Flask
app = Flask(__name__)

# Carrega o modelo (regras) na inicialização do app
MODEL_PATH = "rules.pkl"
try:
    with open(MODEL_PATH, 'rb') as f:
        rules = pickle.load(f)
        model_date = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH)).strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Modelo carregado de {MODEL_PATH} (modificado em {model_date})")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    rules = []
    model_date = None

# Endpoint para retornar todas as regras
@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Endpoint para obter todas as regras."""
    if not rules:
        return jsonify({"error": "Nenhum modelo carregado"}), 500
    return jsonify(rules)

# Endpoint para buscar regras baseadas no antecedente
@app.route('/api/rules/search', methods=['GET'])
def search_rules():
    """Endpoint para buscar regras baseadas no antecedente."""
    antecedent = request.args.get('antecedent')
    if not antecedent:
        return jsonify({"error": "O parâmetro 'antecedent' é obrigatório"}), 400

    antecedent_set = set(antecedent.split(","))
    matched_rules = [
        {"antecedent": list(rule[0]), "consequent": list(rule[1]), "confidence": rule[2]}
        for rule in rules if antecedent_set.issubset(rule[0])
    ]
    return jsonify(matched_rules)

# Endpoint para recomendar músicas
@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Endpoint para recomendar músicas com base nos dados do usuário."""
    if not rules:
        return jsonify({"error": "Nenhum modelo carregado"}), 500

    # Obtém o corpo da requisição em JSON
    try:
        data = request.get_json(force=True)
        user_songs = data.get('songs', [])
        if not user_songs:
            return jsonify({"error": "O campo 'songs' é obrigatório e deve conter uma lista de músicas"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {e}"}), 400

    user_songs_set = set(user_songs)
    recommendations = [
        {"antecedent": list(rule[0]), "consequent": list(rule[1]), "confidence": rule[2]}
        for rule in rules if user_songs_set.issubset(rule[0])
    ]

    # Extrai apenas as recomendações (consequentes) únicas
    recommended_songs = {song for rule in recommendations for song in rule["consequent"]}
    recommended_songs -= user_songs_set  # Remove músicas que o usuário já forneceu

    return jsonify({
        "songs": list(recommended_songs),
        "version": "1.0.0",
        "model_date": model_date
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
