# Laadpaal Management Systeem

> Schoolproject in groepsverband.

Dit project is een webapplicatie voor het beheren van laadpalen. De applicatie bestaat uit een Python backend en een PHP frontend, met een MySQL-database.

## Vereisten
- Python 3.12+
- Docker Desktop
- Browser

## Starten
### 1. Start de database
```bash
docker compose up -d
```

### 2. Installeer backend-afhankelijkheden
```bash
cd backend
python -m pip install --user -r requirements.txt
```

### 3. Maak de configuratie aan
Maak in `backend/config/` een bestand `config.py` en kopieer de inhoud van `config.py.example` naar dit bestand. Vul daarna de juiste waarden in.

### 4. Start de backend
```bash
cd backend
python server.py
```

De backend draait dan op: http://localhost:8000

### 5. Open de frontend
Open in je browser:
```text
http://localhost
```

Als alles goed werkt, verschijnt de inlogpagina van het project.