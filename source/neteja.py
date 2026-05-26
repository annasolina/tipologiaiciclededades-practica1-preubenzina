import pandas as pd

# carregar dades
df = pd.read_csv("data/benzineresCatalunya.csv")

# 1. ES_24H
df["es_24h"] = df["horari"].str.upper().str.strip().eq("L-D: 24H")

print(df["es_24h"].value_counts())

# 2. MARCA NORMALITZADA
df["marca_normalitzada"] = df["marca"].str.lower().str.strip()

print(df["marca_normalitzada"].value_counts().head(20))

# 3. TIPUS ESTACIO
urbana = {
    "CALLE", "CL", "C/", "CARRER",
    "AVENIDA", "AVINGUDA",
    "RONDA", "PASEO"
}

carretera = {
    "CARRETERA", "CTRA.", "AUTOPISTA",
    "AUTOVIA", "CAMI", "POLIGONO"
}

def tipus_estacio(direccio):
    
    if pd.isna(direccio):
        return "ciutat_poble"
    
    d = direccio.upper().strip()
    
    if any(x in d for x in carretera):
        return "carretera_autopista"
    
    if any(x in d for x in urbana):
        return "ciutat_poble"
    
    if "CR" in d:
        return "ciutat_poble"
    
    return "ciutat_poble"

df["tipus_estacio"] = df["direccio"].apply(tipus_estacio)

print(df["tipus_estacio"].value_counts())

# 4. GUARDAR RESULTAT FINAL
df.to_csv("data/benzineresCatalunya_clean.csv", index=False)