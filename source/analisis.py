import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
from scipy import stats

# ==============================================================================
# 1. CARREGAR DADES
# ==============================================================================

df = pd.read_csv("data/benzineresCatalunya_netejat.csv")

# ==============================================================================
# 2. VARIABLES DERIVADES
# ==============================================================================

df["es_24h"] = df["horari"].str.upper().str.strip().eq("L-D: 24H")

top_marques = df["marca"].value_counts().nlargest(15).index
df["marca_reduida"] = df["marca"].apply(
    lambda x: x if x in top_marques else "OTHER"
)

# ==============================================================================
# 3. MODEL SUPERVISAT (REGRESSIÓ LINEAL)
# ==============================================================================

features = ["es_24h", "tipus_estacio", "marca_reduida"]
target = "gasolina_95"

df_sup = df[features + [target]].copy()

df_sup = pd.get_dummies(
    df_sup,
    columns=["es_24h", "tipus_estacio", "marca_reduida"],
    drop_first=True
)

X = df_sup.drop(columns=[target])
y = df_sup[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

print("\nRESULTATS MODEL SUPERVISAT")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

# ==============================================================================
# 4. MODEL NO SUPERVISAT (K-MEANS)
# ==============================================================================

df_cluster = df[["gasolina_95", "es_24h", "tipus_estacio", "marca_reduida"]].copy()

df_cluster = pd.get_dummies(
    df_cluster,
    columns=["es_24h", "tipus_estacio", "marca_reduida"],
    drop_first=True
)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

print("\nDistribució clusters:")
print(df["cluster"].value_counts())

# PCA per visualització
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

df["pca1"] = components[:, 0]
df["pca2"] = components[:, 1]

plt.figure()
plt.scatter(df["pca1"], df["pca2"], c=df["cluster"])
plt.title("Clusters gasolineres (PCA)")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.show()

# ==============================================================================
# 5. CONTRAST D'HIPÒTESI
# ==============================================================================

grup_24h = df[df["es_24h"] == True]["gasolina_95"].dropna()
grup_no_24h = df[df["es_24h"] == False]["gasolina_95"].dropna()

# Normalitat
shapiro_24h = stats.shapiro(grup_24h.sample(min(len(grup_24h), 500), random_state=42))
shapiro_no = stats.shapiro(grup_no_24h.sample(min(len(grup_no_24h), 500), random_state=42))

print("\nNORMALITAT (Shapiro-Wilk)")
print(f"24h p-value: {shapiro_24h.pvalue:.5f}")
print(f"No 24h p-value: {shapiro_no.pvalue:.5f}")

# Homocedasticitat
levene_test = stats.levene(grup_24h, grup_no_24h)

print("\nHOMOCEDASTICITAT (Levene)")
print(f"p-value: {levene_test.pvalue:.5f}")

# T-test
t_test = stats.ttest_ind(grup_24h, grup_no_24h, equal_var=False)

print("\nT-TEST (24h vs no 24h)")
print(f"p-value: {t_test.pvalue:.5f}")
print(f"t-statistic: {t_test.statistic:.5f}")

# Mitjanes
print("\nMITJANES")
print(f"Preu mitjà 24h: {grup_24h.mean():.4f}")
print(f"Preu mitjà no 24h: {grup_no_24h.mean():.4f}")