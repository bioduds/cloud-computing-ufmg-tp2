import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import logging
import os

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configurações
DATASET_PATHS = [
    "/home/datasets/spotify/2023_spotify_ds1.csv",
    "/home/datasets/spotify/2023_spotify_ds2.csv",
]
OUTPUT_FILE = "rules.pkl"
MIN_SUPPORT_RATIO = 0.4
MIN_CONFIDENCE = 0.5
DELIMITER = "\t"


def load_datasets(file_paths, delimiter):
    """
    Carrega os datasets das trilhas fornecidas e combina em uma única lista de conjuntos de itens.
    """
    itemsets = []
    for file_path in file_paths:
        try:
            logging.info(f"Carregando dataset: {file_path}")
            df = pd.read_csv(file_path, sep=delimiter)
            if {'artist_name', 'track_name'}.issubset(df.columns):
                # Cria uma lista de conjuntos baseada em 'artist_name' e 'track_name'
                sets = df[['artist_name', 'track_name']].apply(list, axis=1).tolist()
                itemsets.extend(sets)
                logging.info(f"Carregados {len(sets)} conjuntos de itens do arquivo {file_path}")
            else:
                logging.error(f"Colunas necessárias ausentes em {file_path}. Ignorando...")
        except Exception as e:
            logging.error(f"Erro ao carregar {file_path}: {e}")
    return itemsets


def generate_rules(itemsets, min_support_ratio, min_confidence):
    """
    Gera conjuntos de itens frequentes e regras de associação usando o algoritmo FP-Growth.
    """
    logging.info("Gerando conjuntos de itens frequentes e regras...")
    freq_itemsets, rules = fpgrowth(itemsets, minSupRatio=min_support_ratio, minConf=min_confidence)
    logging.info(f"Gerados {len(freq_itemsets)} conjuntos de itens frequentes e {len(rules)} regras")
    return freq_itemsets, rules


def save_rules(rules, output_file):
    """
    Salva as regras geradas em um arquivo utilizando pickle.
    """
    try:
        with open(output_file, 'wb') as f:
            pickle.dump(rules, f)
        logging.info(f"Regras salvas em {output_file}")
    except Exception as e:
        logging.error(f"Erro ao salvar as regras: {e}")


def main():
    # Carrega os datasets
    itemsets = load_datasets(DATASET_PATHS, DELIMITER)
    if not itemsets:
        logging.error("Nenhum conjunto de itens foi carregado. Encerrando...")
        return

    # Gera conjuntos de itens frequentes e regras
    freq_itemsets, rules = generate_rules(itemsets, MIN_SUPPORT_RATIO, MIN_CONFIDENCE)

    # Salva as regras em um arquivo
    save_rules(rules, OUTPUT_FILE)

    # Exibe os resultados (para depuração ou análise)
    print("Conjuntos de Itens Frequentes:", freq_itemsets)
    print("Regras Geradas:", rules)


if __name__ == "__main__":
    main()
