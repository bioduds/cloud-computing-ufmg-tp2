import requests
import sys
import json

BASE_URL = "http://localhost:8000/api"

def get_all_rules():
    """
    Busca e exibe todas as regras do servidor.
    """
    try:
        # Envia uma solicitação GET para obter todas as regras
        response = requests.get(f"{BASE_URL}/rules")
        response.raise_for_status()
        rules = response.json()
        print("Todas as Regras:")
        # Exibe cada regra no formato legível
        for rule in rules:
            print(f"Antecedente: {rule[0]}, Consequente: {rule[1]}, Confiança: {rule[2]}")
    except requests.RequestException as e:
        # Trata erros relacionados à requisição
        print(f"Erro ao buscar regras: {e}")

def search_rules(antecedent):
    """
    Busca regras com base no antecedente fornecido.
    """
    try:
        # Envia uma solicitação GET para buscar regras específicas com base no antecedente
        response = requests.get(f"{BASE_URL}/rules/search", params={"antecedent": antecedent})
        response.raise_for_status()
        rules = response.json()
        print(f"Regras para o antecedente '{antecedent}':")
        # Exibe as regras correspondentes de forma legível
        for rule in rules:
            print(f"Antecedente: {rule['antecedent']}, Consequente: {rule['consequent']}, Confiança: {rule['confidence']}")
    except requests.RequestException as e:
        # Trata erros relacionados à requisição
        print(f"Erro ao buscar regras: {e}")

def recommend_songs(songs):
    """
    Solicita recomendações de músicas com base na lista fornecida.
    """
    try:
        # Define os dados no formato JSON
        data = {"songs": songs}
        headers = {"Content-Type": "application/json"}
        # Envia uma solicitação POST para obter recomendações
        response = requests.post(f"{BASE_URL}/recommend", data=json.dumps(data), headers=headers)
        response.raise_for_status()
        recommendations = response.json()
        print("Músicas Recomendadas:")
        # Exibe as músicas recomendadas
        for song in recommendations["songs"]:
            print(f"- {song}")
        # Exibe informações adicionais sobre o modelo usado
        print(f"Versão do Modelo: {recommendations['version']}")
        print(f"Data do Modelo: {recommendations['model_date']}")
    except requests.RequestException as e:
        # Trata erros relacionados à requisição
        print(f"Erro ao obter recomendações: {e}")

def main():
    """
    Interface CLI principal para o cliente.
    """
    print("Bem-vindo ao Cliente de Recomendação de Playlists!")
    print("Escolha uma opção:")
    print("1. Buscar todas as regras")
    print("2. Buscar regras por antecedente")
    print("3. Obter recomendações de músicas")
    print("4. Sair")
    
    while True:
        # Solicita a entrada do usuário para navegar no menu
        choice = input("\nDigite sua escolha: ")
        if choice == "1":
            # Opção para buscar todas as regras
            get_all_rules()
        elif choice == "2":
            # Opção para buscar regras por antecedente
            antecedent = input("Digite o antecedente (separado por vírgulas): ")
            search_rules(antecedent)
        elif choice == "3":
            # Opção para solicitar recomendações de músicas
            songs = input("Digite as músicas (separadas por vírgulas): ").split(",")
            recommend_songs([song.strip() for song in songs])
        elif choice == "4":
            # Opção para sair do programa
            print("Saindo. Até mais!")
            sys.exit(0)
        else:
            # Mensagem de erro para escolha inválida
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
