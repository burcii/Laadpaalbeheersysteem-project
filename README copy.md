# Laadpaal Management Systeem
Dit project bevat een eenvoudige backend (Python + MySQL) en frontend (PHP/CSS/JS) voor het Laadpaal Management Systeem.
---
## Vereisten, zorg dat je deze geinstalleerd hebt:
- Python 3.12+
- Docker Desktop
- Browser (Chrome, Firefox, etc.)
## Setup
### 0. Startup
Zorg dat Docker op de achtergrond draait
### 1. Backend
1. Start de database met Docker Compose:

```bash
docker compose up -d
````

2. Installeer Python dependencies:

```bash
cd backend
python -m pip install --user -r requirements.txt
```

3. Maak een bestand in backend/config genaamd config.py

4. Kopieer de inhoud van config.py.example naar config.py en vul de velden in.

5. Start de backend server:

```bash
python server.py
```

De backend draait nu op: [http://localhost:8000](http://localhost:8000)

---

### 2. Frontend
1. Open [http://localhost](http://localhost) in je browser.
2. De backend serveert automatisch de frontend.
3. De frontend haalt automatisch de messages op van de backend en toont deze.
4. Als alles correct werkt zie je de login pagina.

---

## Veelvoorkomende issues

* **CORS fouten** → start backend via `server.py` en frontend vanaf hetzelfde domein of via `localhost`.
* **Python kan niet gevonden worden op windows** → check of python in je path staat. Zoek in windows naar environment variables. 
Deze staan in de system properties op de advanced settings tab rechts onder. Voeg `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313` 
en `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Scripts`
toe als ze nog niet in je path staan. Herstart de terminal. Als dit het probleem nog niet oplost kun je in windows zoeken naar manage app aliases. 
zet op deze pagina alles met python in de naam uit. Herstart de terminal.Als dit het probleem nog steeds niet oplost kun je navigeren naar `C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps` 
en verwijder alles gerelateerd aan python. Herstart de terminal.

---

## Opzetten van een Virtuele Omgeving (Aanbevolen voor Mac en Linux gebruikers)

Om afhankelijkheden gescheiden te houden en te voorkomen dat de systeem-Python beschadigd raakt, gebruik je het beste een virtuele omgeving.

```bash
# Maak een virtuele omgeving in de projectmap
python3 -m venv venv

# Activeer de virtuele omgeving
source venv/bin/activate

# Installeer de vereiste pakketten
pip install -r requirements.txt

# Elke keer dat je terugkomt naar het project, activeer je de omgeving opnieuw met:
source venv/bin/activate
```
---

## Database updaten

Wanneer er wijzigingen zijn in de database-structuur (bijvoorbeeld nieuwe tabellen, kolommen of constraints), moet je de databasecontainers opnieuw opbouwen. Hieronder vind je de stappen:

### 1. Stop de database containers

Stop de draaiende containers. Als je -v gebruikt wordt de database volume ook meten verwijderd.
Let wel op dat dit al de data in de database verwijderd.

```bash
docker compose down -v
```

### 2. Start en rebuild de containers

Start de containers opnieuw op. Door een herstart via up -d worden de nieuwste wijzigingen toegepast.

```bash
docker compose up -d
```
* ```-d``` → draait de containers in de achtergrond.

### 3. Verwijderd de ongebruikte volumes

Na een update kunnen oude volumes achterblijven die niet meer gebruikt worden. Deze kun je verwijderen om schijfruimte vrij te maken:

```bash
docker volume prune
```

Je krijgt een bevestigingsvraag:

```bash
Are you sure you want to continue? [y/N] y
```

Typ ```y``` om door te gaan. **Let op**: hiermee worden alle ongebruikte volumes verwijderd, dus ook die van andere projecten.