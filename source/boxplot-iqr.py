# 3.3

import os
import matplotlib.pyplot as plt
import pandas as pd

# RUTES LOCALS 

# Carpeta arrel del projecte (ajusta si cal)
ruta_carpeta = "data"

# Fitxer netejat
ruta_netejat = os.path.join(ruta_carpeta, "benzineresCatalunya_netejat.csv")

# Carregar dataset
df = pd.read_csv(ruta_netejat)

# BOXPLOTS

# Gràfic 1: Gasoil
df.boxplot(column=["gasoil"])
plt.title("Boxplot de Gasoil")
plt.ylabel("Preu (€/Litre)")
plt.show()

# Gràfic 2: Gasolina 95
df.boxplot(column=["gasolina_95"])
plt.title("Boxplot de Gasolina 95")
plt.ylabel("Preu (€/Litre)")
plt.show()

# CÀLCUL REGLE IQR

def calcular_iqr(columna):
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)
    iqr = q3 - q1

    limit_inferior = q1 - 1.5 * iqr
    limit_superior = q3 + 1.5 * iqr

    outliers = df[(df[columna] < limit_inferior) | (df[columna] > limit_superior)]

    print(f"\nResultats per a {columna}:")
    print(f"  - Límits acceptables: [{limit_inferior:.3f} a {limit_superior:.3f}]")
    print(f"  - Nombre de valors extrems detectats: {len(outliers)}")


calcular_iqr("gasoil")
calcular_iqr("gasolina_95")