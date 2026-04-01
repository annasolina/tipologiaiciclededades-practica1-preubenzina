import requests
from bs4 import BeautifulSoup
import csv
import time
import os

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
                table = soup.find("table")

                if not box or not table:
                    continue

                divs = box.find_all("div")

                marca = direccio = poblacio = horari = "-"

                try:
                    marca = divs[0].text.split("Marca:")[1].strip()
                    direccio = divs[1].text.split("Dirección:")[1].strip()
                    poblacio = divs[2].text.split("Población:")[1].strip()
                    horari = divs[3].text.split("Horario:")[1].strip()
                except:
                    pass

                preu_gasoleo_a = "-"
                preu_gasolina_95 = "-"

                for r in table.find_all("tr"):
                    cols = r.find_all("td")
                    if len(cols) == 2:
                        fuel = cols[0].text.strip()
                        price = cols[1].text.strip()

                        if "Gasóleo A" in fuel:
                            preu_gasoleo_a = price

                        if "Gasolina 95" in fuel:
                            preu_gasolina_95 = price

                provincia = prov_url.split("-en-")[-1]
                municipi = muni_url.split("precio-de-gasolina-95-")[-1]

                data.append([
                    provincia,
                    municipi,
                    poblacio,
                    marca,
                    direccio,
                    horari,
                    preu_gasoleo_a,
                    preu_gasolina_95,
                    gas_url
                ])

                print("OK:", marca, poblacio)

                time.sleep(0.4)

            except Exception as e:
                print("ERROR gasolinera:", gas_url, e)

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
        "gasoleo_a",
        "gasolina_95",
        "url"
    ])
    writer.writerows(data)

print("\nCSV creat correctament ✔")
print("Files extretes:", len(data))