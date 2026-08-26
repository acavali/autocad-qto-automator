import pandas as pd
from datetime import datetime

print("--- BIM Automator Milano ---")
print(f"Generato: {datetime.now()}")
print("Tool per automatizzare computo metrico per AutoCAD")

# Simulando dados que viriam de um DWG
dados = [
    {"Elemento": "Parede 15cm", "Quantita": 125.5, "Unita": "m²", "Codice": "W-01"},
    {"Elemento": "Porta 80x210", "Quantita": 8, "Unita": "pz", "Codice": "D-01"},
    {"Elemento": "Finestra 120x120", "Quantita": 5, "Unita": "pz", "Codice": "F-01"},
    {"Elemento": "Pavimento gres", "Quantita": 98.2, "Unita": "m²", "Codice": "FL-01"},
]

df = pd.DataFrame(dados)
df.to_excel("computo_metrico.xlsx", index=False)

print("\n✅ Computo generato con successo!")
print(f"📁 File: computo_metrico.xlsx")
print(f"📊 Totale elementi: {len(df)}")