📄 Català

## Descripció
Aquest projecte consisteix en un script de web scraping que navega per la pàgina web de ClickGasoil per recollir informació detallada de les benzineres de les províncies de Barcelona, Tarragona, Lleida i Girona.

## Dades extretes
El dataset generat inclou els següents camps:
- Província i municipi
- Marca o operador (Repsol, Cepsa, BonÀrea, etc.)
- Adreça i horari d’obertura
- Preu de la Gasolina 95 i del Gasoil A
- URL de la font original
- Data d’extracció

## Scripts del projecte
A més de l’script principal de scraping, el projecte inclou els següents scripts addicionals:

- `source/scraper.py` → Extracció de dades des de la web de ClickGasoil.
- `source/neteja.py` → Procés de neteja i preparació de dades corresponent als apartats 3.1 i 3.2 de la pràctica.
- `source/boxplot-iqr.py` → Anàlisi de valors extrems i detecció d’outliers mitjançant boxplots i IQR (apartat 3.3).
- `source/analisis.py` → Anàlisi exploratòria i estadística de les dades corresponent a l’apartat 4.

## Instal·lació
Per executar l’script, és necessari tenir instal·lat Python 3 i les següents llibreries:
pip install -r requirements.txt

📄 English

## Description
This project consists of a web scraping script that navigates through the ClickGasoil website to collect detailed information about gas stations in the provinces of Barcelona, Tarragona, Lleida, and Girona.

## Extracted Data
The generated dataset includes the following fields:
- Province and municipality
- Brand/operator (Repsol, Cepsa, BonÀrea, etc.)
- Address and opening hours
- Gasoline 95 and Diesel (Gasóleo A) prices
- Source URL
- Extraction date

## Project Scripts
In addition to the main scraping script, the project includes the following additional scripts:

- `source/scraper.py` → Data extraction from the ClickGasoil website.
- `source/neteja.py` → Data cleaning and preprocessing process corresponding to sections 3.1 and 3.2 of the assignment.
- `source/boxplot-iqr.py` → Outlier detection and extreme value analysis using boxplots and IQR (section 3.3).
- `source/analisis.py` → Exploratory and statistical data analysis corresponding to section 4.

## Installation
To run the script, you need Python 3 installed along with the required libraries:
pip install -r requirements.txt