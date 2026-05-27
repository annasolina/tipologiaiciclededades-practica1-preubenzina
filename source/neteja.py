import pandas as pd

# ==============================================================================
# RUTES DELS FITXERS
# ==============================================================================

# Dataset original
ruta_entrada = "data/benzineresCatalunya.csv"

# Dataset netejat final
ruta_sortida = "data/benzineresCatalunya_netejat.csv"

# ==============================================================================
# PAS 1. CARREGAR DATASET
# ==============================================================================

df = pd.read_csv(ruta_entrada)

# ==============================================================================
# 3.1 NETEJA DE PREUS
# ==============================================================================

# Pas 1.1. Convertim els preus a text i netegem el símbol '€'
df["gasoil"] = (
    df["gasoil"]
    .astype(str)
    .str.replace("€", "", regex=False)
    .str.strip()
)

df["gasolina_95"] = (
    df["gasolina_95"]
    .astype(str)
    .str.replace("€", "", regex=False)
    .str.strip()
)

# Pas 1.2. Transformem els guions "-" o strings buits en nuls reals
df["gasoil"] = df["gasoil"].replace("-", None)
df["gasolina_95"] = df["gasolina_95"].replace("-", None)

# Pas 1.3. Convertim els preus a decimals (float)
df["gasoil"] = df["gasoil"].astype(float)
df["gasolina_95"] = df["gasolina_95"].astype(float)

# ==============================================================================
# COMPROVACIÓ INICIAL
# ==============================================================================

print("RECOMPTE INICIAL DE BUITS - PREIMPUTACIÓ")
print(f"Valors nuls inicials en Gasoil: {df['gasoil'].isna().sum()}")
print(f"Valors nuls inicials en Gasolina 95: {df['gasolina_95'].isna().sum()}")

# ==============================================================================
# IMPUTACIÓ DE VALORS NULS
# ==============================================================================

# Imputació per marca i municipi
df["gasoil"] = df["gasoil"].fillna(
    df.groupby(["marca", "municipi"])["gasoil"].transform("mean")
)

df["gasolina_95"] = df["gasolina_95"].fillna(
    df.groupby(["marca", "municipi"])["gasolina_95"].transform("mean")
)

# Si encara hi ha buits → mitjana del municipi
df["gasoil"] = df["gasoil"].fillna(
    df.groupby("municipi")["gasoil"].transform("mean")
)

df["gasolina_95"] = df["gasolina_95"].fillna(
    df.groupby("municipi")["gasolina_95"].transform("mean")
)

# Si encara hi ha buits → mitjana de la província
df["gasoil"] = df["gasoil"].fillna(
    df.groupby("provincia")["gasoil"].transform("mean")
)

df["gasolina_95"] = df["gasolina_95"].fillna(
    df.groupby("provincia")["gasolina_95"].transform("mean")
)

# ==============================================================================
# COMPROVACIÓ FINAL
# ==============================================================================

print("\nRECOMPTE FINAL DESPRÉS D'IMPUTAR")
print(f"Valors nuls finals en Gasoil: {df['gasoil'].isna().sum()}")
print(f"Valors nuls finals en Gasolina 95: {df['gasolina_95'].isna().sum()}")

# ==============================================================================
# 3.2 TRANSFORMACIÓ DE VARIABLES
# ==============================================================================

# ------------------------------------------------------------------------------
# Variable es_24h
# ------------------------------------------------------------------------------

df["es_24h"] = (
    df["horari"]
    .str.upper()
    .str.strip()
    .eq("L-D: 24H")
)

print("\nRECOMPTE VARIABLE es_24h")
print(df["es_24h"].value_counts())

# ------------------------------------------------------------------------------
# Variable marca_normalitzada
# ------------------------------------------------------------------------------

df["marca_normalitzada"] = (
    df["marca"]
    .str.lower()
    .str.strip()
)

print("\nTOP 20 MARQUES NORMALITZADES")
print(df["marca_normalitzada"].value_counts().head(20))

# ------------------------------------------------------------------------------
# Variable tipus_estacio
# ------------------------------------------------------------------------------

urbana = {
    "CALLE",
    "CL",
    "C/",
    "CARRER",
    "AVENIDA",
    "AVINGUDA",
    "RONDA",
    "PASEO"
}

carretera = {
    "CARRETERA",
    "CTRA.",
    "AUTOPISTA",
    "AUTOVIA",
    "CAMI",
    "POLIGONO"
}

def tipus_estacio(direccio):

    if pd.isna(direccio):
        return "ciutat_poble"

    d = direccio.upper().strip()

    # Estacions carretera/autopista
    if any(x in d for x in carretera):
        return "carretera_autopista"

    # Estacions urbanes
    if any(x in d for x in urbana):
        return "ciutat_poble"

    # Cas ambigu "CR"
    if "CR" in d:
        return "ciutat_poble"

    # Valor per defecte
    return "ciutat_poble"

df["tipus_estacio"] = df["direccio"].apply(tipus_estacio)

print("\nTIPUS D'ESTACIÓ")
print(df["tipus_estacio"].value_counts())

# ==============================================================================
# GUARDAR RESULTAT FINAL
# ==============================================================================

df.to_csv(ruta_sortida, index=False)

print(f"\n✔ Fitxer guardat correctament a: {ruta_sortida}")