# Umzug zu Render.com — Anleitung für später

Diese Anleitung führt dich durch den kompletten Umzug deiner Seite von
"läuft auf meinem PC + cloudflared" zu "läuft dauerhaft in der Cloud bei
Render.com". Die Dateien dafür sind schon vorbereitet (`Procfile`,
`gunicorn` in `requirements.txt`, ein `/ping`-Endpunkt).

Du brauchst dafür: einen PC mit Internetzugang, ca. 20-30 Minuten Zeit,
keine Kreditkarte nötig.

---

## Teil 1: Code zu GitHub hochladen

Render lädt deine Seite direkt aus einem GitHub-Repository. Falls du noch
kein GitHub-Konto hast:

1. Gehe zu https://github.com/signup und erstelle ein kostenloses Konto
2. Klicke oben rechts auf **"+"** → **"New repository"**
3. Name z.B. `max-luka-tv`, auf **"Public"** oder **"Private"** stellen
   (beides ist ok), **NICHT** mit README/gitignore initialisieren
4. Lade deinen kompletten Projektordner dort hoch. Am einfachsten dafür:
   - Auf der neuen, leeren Repository-Seite auf **"uploading an existing
     file"** klicken
   - Alle Dateien aus deinem `max-luka-tv`-Ordner per Drag & Drop
     reinziehen (app.py, requirements.txt, Procfile, templates/, static/,
     README.md - **NICHT** den `venv`-Ordner, falls vorhanden)
   - Unten auf **"Commit changes"** klicken

## Teil 2: Render-Konto erstellen und Seite deployen

1. Gehe zu https://render.com und erstelle ein kostenloses Konto
   (Anmeldung z.B. direkt mit deinem GitHub-Konto möglich - spart einen
   Schritt)
2. Im Dashboard auf **"New +"** → **"Web Service"** klicken
3. Dein gerade hochgeladenes GitHub-Repository `max-luka-tv` auswählen
   und verbinden
4. Einstellungen (falls nicht automatisch erkannt):
   - **Name**: z.B. `max-luka-tv`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free** auswählen
5. Bei **"Environment Variables"** (wichtig für deinen API-Key):
   - Klicke **"Add Environment Variable"**
   - Key: `YOUTUBE_API_KEY`
   - Value: dein echter YouTube-API-Key
   - (Das ist sicherer als den Key im Code zu lassen - auch wenn er
     aktuell noch als Rückfallwert in `app.py` steht, funktioniert es so
     oder so)
6. Auf **"Create Web Service"** klicken

Render baut jetzt deine Seite (dauert 1-3 Minuten). Du bekommst eine
Adresse wie `https://max-luka-tv.onrender.com` - probier die direkt mal
aus, sobald der Status auf "Live" springt.

## Teil 3: Eigene Domain (www.max-lukatv.com) verbinden

1. In Render bei deinem Web-Service auf **"Settings"** → **"Custom
   Domains"** gehen
2. **"Add Custom Domain"** klicken, `www.max-lukatv.com` eingeben
3. Render zeigt dir einen CNAME-Zielwert (etwas wie
   `max-luka-tv.onrender.com`)
4. Wechsle zu Cloudflare (dash.cloudflare.com) → deine Domain → **DNS** →
   **Records**
5. Den bestehenden `www`-Eintrag (aktuell zeigt er auf deinen Tunnel)
   bearbeiten: **Type** bleibt CNAME, **Content/Target** auf den von
   Render gezeigten Wert ändern, **Proxy-Status** auf "DNS only" (graue
   Wolke) stellen für die Ersteinrichtung
6. Ein paar Minuten warten, dann `https://www.max-lukatv.com` testen

## Teil 4: Alten Tunnel abschalten (optional, danach)

Sobald Render zuverlässig läuft, brauchst du dein `python app.py` und
`cloudflared tunnel run` auf deinem PC nicht mehr. Du kannst die
Fenster einfach schließen und deinen PC ganz normal aus- und wieder
einschalten - deine Seite bleibt trotzdem online, weil sie jetzt bei
Render läuft statt auf deinem PC.

## Teil 5 (optional): Damit die Seite nie einschläft

Der kostenlose Render-Plan lässt die Seite nach 15 Minuten ohne Besuch
einschlafen (nächster Besucher wartet dann 30-60 Sekunden). Das kannst
du mit einem kostenlosen "Wach-halte"-Dienst vermeiden:

1. Gehe zu https://uptimerobot.com und erstelle ein kostenloses Konto
2. **"Add New Monitor"** klicken
3. Monitor Type: **HTTP(s)**
4. URL: `https://www.max-lukatv.com/ping` (das ist der extra dafür
   vorbereitete, leichte Endpunkt - belastet nicht deine YouTube-API)
5. Monitoring-Intervall: **5 Minuten**
6. Speichern

Damit "besucht" UptimeRobot deine Seite alle 5 Minuten von selbst, sie
schläft praktisch nie mehr ein - komplett kostenlos und automatisch,
ohne dass du etwas tun musst.

---

## Zusammenfassung: was sich für dich ändert

| Vorher (jetzt) | Nachher (mit Render) |
|---|---|
| PC muss an sein | PC kann komplett aus sein |
| 2 Terminal-Fenster müssen laufen | Nichts muss laufen |
| Sofort erreichbar, wenn PC an | Meist sofort, manchmal 30-60 Sek. Wartezeit (außer mit UptimeRobot) |
| Kostenlos | Kostenlos |

Bei Fragen während der Umsetzung: einfach wieder melden, Screenshots
schicken, ich helfe dir Schritt für Schritt genau wie beim
Cloudflare-Setup.
