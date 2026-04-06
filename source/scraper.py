import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.clickgasoil.com"

start_url = "https://www.clickgasoil.com/c/precio-gasolina-95-catalua"

# =========================
# CARPETA SEGURA
# =========================
os.makedirs("data", exist_ok=True)

data = []

# =========================
# 1. PROVÍNCIES
# =========================
response = requests.get(start_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

provincies = [
    base_url + a["href"]
    for a in soup.find_all("a")
    if a.get("href") and "/p/precio-gasolina-95-en-" in a.get("href")
]

# =========================
# 2. LOOP PROVÍNCIES
# =========================
for prov_url in provincies:
    print("\nPROVÍNCIA:", prov_url)

    soup = BeautifulSoup(requests.get(prov_url, headers=headers).text, "html.parser")

    municipis = [
        base_url + a["href"]
        for a in soup.find_all("a")
        if a.get("href") and "/m/precio-de-gasolina-95-" in a.get("href")
    ]

    # =========================
    # 3. MUNICIPIS
    # =========================
    for muni_url in municipis:
        print("  Municipi:", muni_url)

        soup = BeautifulSoup(requests.get(muni_url, headers=headers).text, "html.parser")

        gasolineras = [
            base_url + a["href"]
            for a in soup.find_all("a")
            if a.get("href") and "/g/" in a.get("href")
        ]

        # =========================
        # 4. BENZINERES
        # =========================
        for gas_url in gasolineras:

            try:
                soup = BeautifulSoup(requests.get(gas_url, headers=headers).text, "html.parser")

                box = soup.find("div", class_="datos_gasolinera")
                tables = soup.find_all("table")

                if not box or not tables:
                    continue

                target_table = None
                for t in tables:
                    if "Precio" in t.text or "Carburante" in t.text or "95" in t.text:
                        target_table = t
                        break
                
                if not target_table:
                    continue

                
                text_complet = box.get_text(separator="\n", strip=True)
                linies = text_complet.split("\n")

                marca = direccio = poblacio = horari = "-"

                try:
                    for i, linia in enumerate(linies):
                        if "Marca:" in linia:
                           
                            if linia.strip() == "Marca:" and i+1 < len(linies):
                                marca = linies[i+1].strip()
                            else:
                                marca = linia.split(":", 1)[1].strip()
                                
                        if "Direcci" in linia:
                            if linia.strip().startswith("Direcci") and i+1 < len(linies):
                                direccio = linies[i+1].strip()
                            else:
                                direccio = linia.split(":", 1)[1].strip()
                                
                        if "Poblaci" in linia:
                            if linia.strip().startswith("Poblaci") and i+1 < len(linies):
                                poblacio = linies[i+1].strip()
                            else:
                                poblacio = linia.split(":", 1)[1].strip()
                                
                        if "Horario:" in linia:
                            if linia.strip() == "Horario:" and i+1 < len(linies):
                                horari = linies[i+1].strip()
                            else:
                                horari = linia.split(":", 1)[1].strip()
                
                
                except:
                    pass

                preu_gasoil = "-"
                preu_gasolina_95 = "-"

                data_extraccio = datetime.now().strftime("%d/%m/%Y")

                for r in target_table.find_all("tr"):
                    cols = r.find_all("td")
                    if len(cols) >= 2:
                        fuel = cols[0].get_text(strip=True).lower()
                        price = cols[1].get_text(strip=True)
                        
                        if "95" in fuel:
                            preu_gasolina_95 = price
                        elif "óleo a" in fuel or "oleo a" in fuel or "gasoleo" in fuel:
                            preu_gasoil= price


              

                provincia = prov_url.split("-en-")[-1]
                municipi = muni_url.split("precio-de-gasolina-95-")[-1]

                data.append([
                    provincia,
                    municipi,
                    poblacio,
                    marca,
                    direccio,
                    horari,
                    preu_gasoil,
                    preu_gasolina_95,
                    data_extraccio,
                    gas_url
                ])

                print(f"OK: {marca} | G95: {preu_gasolina_95} | GA: {preu_gasoil}")
                time.sleep(0.4) #Robots diu 10s pero hem comprat amb 0.4s i funciona

            except Exception as e:
                print(f"    ERROR gasolinera: {gas_url} | {e}")

# =========================
# 5. CSV FINAL
# =========================
file_path = "data/benzineresCatalunya.csv"

with open(file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "provincia",
        "municipi",
        "poblacio",
        "marca",
        "direccio",
        "horari",
        "gasoil",
        "gasolina_95",
        "data_extraccio",
        "url"
    ])
    writer.writerows(data)

print("\nCSV creat correctament ✔")
print("Files extretes:", len(data))