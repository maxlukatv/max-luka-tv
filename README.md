# Max-Luka TV — Webseite

Eine kleine Webseite mit Flask (Python) rund um deinen YouTube-Kanal
**@max-lukatv**: Infos über dich, deine **neuesten Videos** und deine
**Top Videos** (nach Aufrufen) werden automatisch über die YouTube Data API
geladen — dazu Links zu Instagram und deiner WhatsApp-Community. Du kannst
die Seite lokal starten und über **cloudflared** kostenlos im Internet
freigeben — ganz ohne eigenen Server oder Domain.

## Projektstruktur

```
max-luka-tv/
├── app.py                 <- Flask-Server + deine Daten + YouTube-Anbindung
├── requirements.txt
├── templates/
│   └── index.html         <- HTML-Struktur der Seite
└── static/
    ├── css/style.css      <- Design
    └── js/script.js       <- kleine Animationen
```

## 1. YouTube API-Key einrichten (für automatische Videos)

Damit "Neueste Videos" und "Top Videos" automatisch geladen werden, brauchst
du einen **kostenlosen** YouTube-Data-API-Key von Google:

1. Gehe zu <https://console.cloud.google.com/>
2. Oben ein neues Projekt anlegen (z. B. "max-luka-tv")
3. Im Menü zu **APIs & Dienste → Bibliothek** und nach **"YouTube Data API v3"**
   suchen → **aktivieren**
4. Zu **APIs & Dienste → Anmeldedaten** → **Anmeldedaten erstellen →
   API-Schlüssel** → der Key wird angezeigt, kopieren
5. Den Key in `app.py` bei `YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "DEIN_API_KEY_HIER")`
   anstelle von `DEIN_API_KEY_HIER` einfügen

> 💡 Der kostenlose Kontingent-Rahmen (10.000 Einheiten/Tag) reicht für eine
> Seite wie diese locker aus — die Videos werden zusätzlich 10 Minuten lang
> zwischengespeichert (`CACHE_SECONDS` in `app.py`), damit nicht bei jedem
> Seitenaufruf neu abgefragt wird.

> 🔒 Sicherheitstipp: Trage den Key alternativ als Umgebungsvariable ein,
> statt ihn direkt im Code zu speichern (besonders wenn du den Code mal
> irgendwo hochlädst, z. B. auf GitHub):
> ```powershell
> $env:YOUTUBE_API_KEY = "dein-key-hier"
> ```
> Das gilt dann nur für das aktuelle Terminal-Fenster.

Ohne API-Key läuft die Seite trotzdem — dann erscheint statt der Videos ein
Hinweis, dass der Key noch fehlt.

## 2. Eigene Inhalte eintragen

Öffne `app.py`. Diese Blöcke kannst du anpassen:

- **`CHANNEL_ID`** – deine YouTube-Kanal-ID (für @max-lukatv schon eingetragen)
- **`CHANNEL`** – Name, Tagline, Bio-Text, Status
- **`LINKS`** – deine echten Links (Instagram-Profil, WhatsApp-Community-
  Einladungslink "Schiene und Weiche", ...). Weitere Plattformen kannst du
  als neuen Eintrag hinzufügen (z. B. TikTok, Twitch, Discord — Icons sind
  im CSS schon vorbereitet, einfach `"icon": "tiktok"` o. Ä. setzen)
- **`LATEST_VIDEOS_COUNT`** / **`TOP_VIDEOS_COUNT`** – wie viele Videos
  jeweils angezeigt werden

Einfach die Platzhalter-Texte (z. B. `DEIN-PROFIL`) durch deine echten Daten
ersetzen und speichern.

## 3. Python-Umgebung einrichten

Im Terminal, im Ordner `max-luka-tv`:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Seite lokal starten

```bash
python3 app.py
```

Die Seite läuft jetzt unter `http://localhost:5050`. Öffne die Adresse im
Browser und schau, ob alles passt. Nach Änderungen an `app.py` einfach die
Seite im Browser neu laden (dank `debug=True` lädt Flask automatisch neu).

## 5. cloudflared installieren

Falls noch nicht vorhanden:

- **Windows:** `winget install --id Cloudflare.cloudflared`
- **macOS:** `brew install cloudflared`
- **Linux (Debian/Ubuntu):**
  ```bash
  curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
  sudo dpkg -i cloudflared.deb
  ```

Prüfen, ob es funktioniert:

```bash
cloudflared --version
```

## 6. Seite mit cloudflared veröffentlichen

Bei laufendem Flask-Server (`python3 app.py`, Schritt 3) in einem **zweiten**
Terminal-Fenster:

```bash
cloudflared tunnel --url http://localhost:5050
```

cloudflared gibt dir daraufhin eine Adresse aus wie:

```
https://irgendwas-zufaellig.trycloudflare.com
```

Diesen Link kannst du direkt teilen — jeder im Internet kann deine Seite
darüber aufrufen, solange dein Rechner läuft und der Tunnel offen ist.

> ℹ️ Das ist ein **Quick Tunnel** (kostenlos, ohne Cloudflare-Account, ohne
> eigene Domain) — perfekt zum Testen und Teilen. Die Adresse ändert sich bei
> jedem Neustart des Tunnels. Wenn du später eine feste, eigene Domain
> (z. B. `maxlukatv.de`) verwenden möchtest, kannst du einen **benannten
> Tunnel** mit einem kostenlosen Cloudflare-Account einrichten — sag
> einfach Bescheid, dann zeige ich dir das auch.

## Seite beenden

- Tunnel stoppen: im Terminal mit `Strg + C`
- Flask-Server stoppen: im anderen Terminal mit `Strg + C`

## Nächste Schritte / Ideen

- Eigenes Profilbild oder Logo als Datei in `static/img/` ablegen und im
  Template einbinden
- Eigene Domain über Cloudflare verbinden (siehe oben)
- Weitere Seiten hinzufügen (z. B. `/about`, eigene Route in `app.py`)
