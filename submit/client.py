# client.py
import requests

BASE_URL = "http://localhost:8000/api"

# Lendo regras
response = requests.get(f"{BASE_URL}/rules")
print("All Rules:")
print(response.json())

# Buswcando antecedentes
antecedent = "milk,diaper"
response = requests.get(f"{BASE_URL}/rules/search", params={"antecedent": antecedent})
print(f"Rules for antecedent '{antecedent}':")
print(response.json())
