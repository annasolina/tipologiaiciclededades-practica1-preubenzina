# tipologiaiciclededades-practica1-preubenzina
📄 Català

Descripció
Aquest projecte consisteix en un script de web scraping que navega per la pàgina web de ClickGasoil per recollir informació detallada de les benzineres de les províncies de Barcelona, Tarragona, Lleida i Girona.

Dades extretes
El dataset generat inclou els següents camps:
- Província i municipi
- Marca o operador (Repsol, Cepsa, BonÀrea, etc.)
- Adreça i horari d’obertura
- Preu de la Gasolina 95 i del Gasoil A
- URL de la font original
- Data d’extracció

Instal·lació
Per executar l’script, és necessari tenir instal·lat Python 3 i les següents llibreries:
pip install requests
pip install beautifulsoup4
Alternativament, es poden instal·lar totes les dependències amb:
pip install -r requirements.txt

Execució
python3 source/scraper.py

English

Description
This project consists of a web scraping script that navigates through the ClickGasoil website to collect detailed information about gas stations across the provinces of Barcelona, Tarragona, Lleida, and Girona (Catalonia, Spain).

Extracted Data
The generated dataset includes the following fields:
- Province and municipality
- Brand/operator (e.g., Repsol, Cepsa, BonÀrea, etc.)
- Address and opening hours
- Prices for Gasoline 95 and Diesel (Gasóleo A)
- Source URL
- Extraction date

Installation
To run the script, you need Python 3 installed along with the following libraries:
pip install requests
pip install beautifulsoup4
Alternatively, you can install all dependencies using:
pip install -r requirements.txt

Usage
python3 source/scraper.py