"""
Fragen-Datenbank für das Bahnsignale-Lernspiel (/signale_lernen).

Die Inhalte basieren auf dem offiziellen, öffentlich dokumentierten
deutschen Signalsystem (Signalbuch Ril 301 der DB sowie historische
Systeme der ehemaligen Deutschen Bundesbahn/Deutschen Reichsbahn). Alle
Grafiken sind selbst erstellte, vereinfachte SVG-Illustrationen - keine
Bilder von Drittseiten.
"""

import random

# ---------------------------------------------------------------------------
# Kleine SVG-Bausteine für die Signal-Darstellung
# ---------------------------------------------------------------------------

_LAMP_COLORS = {
    "red": "#d21f2f",
    "green": "#1f8a3a",
    "yellow": "#e0a300",
    "white": "#f5f0ec",
    "off": "#3a2f2b",
}


def _licht_signal(lamps, shape="rund"):
    """Signalmast mit 1-3 Lampen. lamps = Liste von Farben, oben nach unten."""
    dot = "circle" if shape == "rund" else "rect"
    parts = ['<svg viewBox="0 0 120 160" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<rect x="55" y="60" width="10" height="90" fill="#5a4d47"/>')
    parts.append('<rect x="20" y="10" width="80" height="' + str(28 * len(lamps) + 14) + '" rx="8" fill="#241c1a"/>')
    y = 28
    for color in lamps:
        fill = _LAMP_COLORS.get(color, "#3a2f2b")
        if dot == "circle":
            parts.append(f'<circle cx="60" cy="{y}" r="12" fill="{fill}"/>')
        else:
            parts.append(f'<rect x="46" y="{y-10}" width="28" height="20" rx="3" fill="{fill}"/>')
        y += 28
    parts.append("</svg>")
    return "".join(parts)


def _tafel_signal(bg="#f5f0ec", stripes=False, label="", label_color="#241c1a"):
    """Rechteckige Signaltafel, optional mit Streifen und Kürzel."""
    parts = ['<svg viewBox="0 0 140 100" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<rect x="10" y="70" width="8" height="30" fill="#5a4d47"/>')
    if stripes:
        parts.append(f'<rect x="10" y="10" width="120" height="70" fill="{bg}"/>')
        for i, x in enumerate(range(10, 130, 24)):
            parts.append(f'<polygon points="{x},80 {x+24},80 {x+12},10" fill="#241c1a" opacity="0.85"/>')
    else:
        parts.append(f'<rect x="10" y="10" width="120" height="70" rx="4" fill="{bg}" stroke="#241c1a" stroke-width="3"/>')
    if label:
        parts.append(
            f'<text x="70" y="55" font-family="monospace" font-size="26" font-weight="700" '
            f'text-anchor="middle" fill="{label_color}">{label}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _raute_signal(label=""):
    """Rautenförmige Tafel (z.B. El-Signale)."""
    parts = ['<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<rect x="55" y="90" width="10" height="45" fill="#5a4d47"/>')
    parts.append('<polygon points="60,10 105,55 60,100 15,55" fill="#f5f0ec" stroke="#241c1a" stroke-width="3"/>')
    if label:
        parts.append(
            f'<text x="60" y="63" font-family="monospace" font-size="20" font-weight="700" '
            f'text-anchor="middle" fill="#241c1a">{label}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _konzept_signal(emoji="🚦"):
    """Generisches Symbol für konzeptionelle Fragen (kein konkretes Lichtbild)."""
    parts = ['<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<circle cx="60" cy="60" r="52" fill="#fff4f2" stroke="#d21f2f" stroke-width="4"/>')
    parts.append(f'<text x="60" y="76" font-size="48" text-anchor="middle">{emoji}</text>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Fragen-Pools nach Schwierigkeitsgrad
# ---------------------------------------------------------------------------

LEICHT = [
    {"code": "Hp0", "frage": "Was bedeutet das Hauptsignal Hp0?", "antwort": "Halt! Vor dem Signal anhalten", "bild": _licht_signal(["red"])},
    {"code": "Hp1", "frage": "Was bedeutet das Hauptsignal Hp1?", "antwort": "Fahrt frei, mit zulässiger Höchstgeschwindigkeit", "bild": _licht_signal(["off", "green"])},
    {"code": "Hp2", "frage": "Was bedeutet das Hauptsignal Hp2?", "antwort": "Fahrt frei, aber mit Langsamfahrt (Geschwindigkeitseinschränkung)", "bild": _licht_signal(["yellow", "green"])},
    {"code": "Vr0", "frage": "Was bedeutet das Vorsignal Vr0?", "antwort": "Halt erwarten - das nächste Hauptsignal zeigt voraussichtlich Halt", "bild": _licht_signal(["yellow", "yellow"], shape="raute")},
    {"code": "Vr1", "frage": "Was bedeutet das Vorsignal Vr1?", "antwort": "Fahrt erwarten - das nächste Hauptsignal zeigt voraussichtlich Fahrt frei", "bild": _licht_signal(["green", "green"], shape="raute")},
    {"code": "Vr2", "frage": "Was bedeutet das Vorsignal Vr2?", "antwort": "Langsamfahrt erwarten - das nächste Hauptsignal zeigt voraussichtlich Hp2", "bild": _licht_signal(["green", "yellow"], shape="raute")},
    {"code": "Sh0", "frage": "Was bedeutet das Rangiersignal Sh0?", "antwort": "Halt für Rangierfahrten", "bild": _licht_signal(["red", "off", "red"])},
    {"code": "Sh1", "frage": "Was bedeutet das Rangiersignal Sh1?", "antwort": "Die Rangierfahrt darf sich in Bewegung setzen", "bild": _licht_signal(["white", "off", "white"])},
    {"code": "Ks1", "frage": "Was bedeutet das Kombinationssignal Ks1?", "antwort": "Fahrt frei (moderne Alternative zu Hp1)", "bild": _licht_signal(["off", "green"])},
    {"code": "Ks2", "frage": "Was bedeutet das Kombinationssignal Ks2?", "antwort": "Fahrt frei mit Langsamfahrt (moderne Alternative zu Hp2)", "bild": _licht_signal(["yellow", "green"])},
    {"code": "Hp0/Sh1", "frage": "Ein Hauptsignal zeigt gleichzeitig Hp0 und Sh1 - was bedeutet das?", "antwort": "Der Halt gilt nur für Zugfahrten - Rangierfahrten dürfen vorbeifahren", "bild": _licht_signal(["red", "white"])},
    {"code": "Ks1-Blinklicht", "frage": "Was bedeutet es, wenn ein Ks1-Signal zusätzlich blinkt?", "antwort": "Fahrt frei, aber das nächste Signal zeigt voraussichtlich Halt (ersetzt die Vr-Funktion)", "bild": _licht_signal(["off", "green"])},
    {"code": "Zg-Spitzensignal", "frage": "Wie erkennt man die Spitze (vorderes Ende) eines fahrenden Zuges bei Nacht?", "antwort": "Am Spitzensignal - weiße Lichter an der Zugspitze", "bild": _konzept_signal("🚄")},
    {"code": "Zg-Schlusssignal", "frage": "Wie erkennt man das Ende (den Schluss) eines Zuges bei Nacht?", "antwort": "Am Schlusssignal - meist zwei rote Lichter oder eine rot-weiße Schlussscheibe", "bild": _konzept_signal("🚋")},
]

MITTEL = [
    {"code": "Zs1", "frage": "Was bedeutet das Zusatzsignal Zs1 (Ersatzsignal)?", "antwort": "Weiterfahrt trotz haltzeigendem Hauptsignal erlaubt", "bild": _tafel_signal(label="Zs1")},
    {"code": "Zs3", "frage": "Wofür steht das Zusatzsignal Zs3 mit einer Zahl?", "antwort": "Geschwindigkeitsanzeiger - die Zahl mal 10 km/h ist die zulässige Geschwindigkeit", "bild": _tafel_signal(label="6", bg="#e8e3df")},
    {"code": "Zs3v", "frage": "Was ist die Aufgabe des Zusatzsignals Zs3v?", "antwort": "Kündigt die Geschwindigkeitsbeschränkung eines Zs3 schon am Vorsignal an", "bild": _tafel_signal(label="6v", bg="#e8e3df")},
    {"code": "Zs6", "frage": "Was bedeutet das Zusatzsignal Zs6?", "antwort": "Rangierfahrt erlaubt, obwohl das Hauptsignal Halt zeigt", "bild": _tafel_signal(label="Zs6")},
    {"code": "Zs7", "frage": "Was bedeutet das Zusatzsignal Zs7 (Vorsichtsignal)?", "antwort": "Weiterfahrt auf Sicht, mit äußerster Vorsicht erlaubt", "bild": _tafel_signal(label="Zs7")},
    {"code": "Zs8", "frage": "Wann darf man laut Zusatzsignal Zs8 an einem Halt zeigenden Signal vorbeifahren?", "antwort": "Nach schriftlichem Befehl des Fahrdienstleiters", "bild": _tafel_signal(label="Zs8")},
    {"code": "Zs12", "frage": "Was erlaubt das Zusatzsignal Zs12?", "antwort": "Vorbeifahrt am Halt zeigenden Signal nach mündlicher Erlaubnis des Fahrdienstleiters", "bild": _tafel_signal(label="Zs12")},
    {"code": "Ne1", "frage": "Wofür steht die Trapeztafel Ne1?", "antwort": "Kennzeichnet ein Hauptsignal, das aus größerer Entfernung schwer erkennbar ist", "bild": _tafel_signal(stripes=True)},
    {"code": "Ne2", "frage": "Wofür steht die Haltetafel Ne2?", "antwort": "Kennzeichnet die Stelle, an der ohne Hauptsignal gehalten werden muss", "bild": _tafel_signal(label="—", bg="#f5f0ec")},
    {"code": "Ne3", "frage": "Wofür steht die Vorsignalbake Ne3?", "antwort": "Kündigt ein bevorstehendes Vorsignal oder eine Vorsignaltafel an", "bild": _tafel_signal(label="/", bg="#f5f0ec")},
    {"code": "Ne5", "frage": "Was kündigt das Kennzeichen Ne5 an?", "antwort": "Eine bevorstehende Schutzstrecke (Vorsicht bei elektrischen Anlagen)", "bild": _tafel_signal(label="El", bg="#e8e3df")},
    {"code": "Ra10", "frage": "Wofür steht die Pfeifentafel Ra10?", "antwort": "Hier muss ein akustisches Signal (Pfeifsignal) gegeben werden", "bild": _tafel_signal(label="P")},
    {"code": "Ra11", "frage": "Wofür steht die Ankündigungstafel Ra11?", "antwort": "Kündigt eine vorübergehende Langsamfahrstelle an", "bild": _tafel_signal(label="La")},
    {"code": "Ra12", "frage": "Wofür steht die Läutesignaltafel Ra12?", "antwort": "Kennzeichnet einen Bahnübergang, der durch Läutesignal gesichert wird", "bild": _tafel_signal(label="L")},
    {"code": "Lf1", "frage": "Was zeigt die Langsamfahrscheibe Lf1 an?", "antwort": "Den Anfang einer Langsamfahrstelle, mit der zulässigen Geschwindigkeit", "bild": _tafel_signal(label="Lf1")},
    {"code": "Lf2", "frage": "Was zeigt die Langsamfahrscheibe Lf2 an?", "antwort": "Das Ende einer Langsamfahrstelle", "bild": _tafel_signal(label="Lf2")},
    {"code": "El1", "frage": "Was bedeutet das Signal El1?", "antwort": "Ankündigung: bald folgt ein Streckenabschnitt ohne Fahrdraht", "bild": _raute_signal("El1")},
    {"code": "El2", "frage": "Was bedeutet das Signal El2?", "antwort": "Hier beginnt der Streckenabschnitt ohne Fahrdraht - Hauptschalter jetzt ausschalten", "bild": _raute_signal("El2")},
    {"code": "El3", "frage": "Was bedeutet das Signal El3?", "antwort": "Hier endet der Streckenabschnitt ohne Fahrdraht - Hauptschalter darf wieder eingeschaltet werden", "bild": _raute_signal("El3")},
    {"code": "Bü-Andreaskreuz", "frage": "Wie heißt das bekannteste Bahnübergangszeichen für Straßenverkehr?", "antwort": "Das Andreaskreuz", "bild": _konzept_signal("✖️")},
]

SCHWER = [
    {"code": "Ne6", "frage": "Wofür steht das Kennzeichen Ne6?", "antwort": "Kennzeichnet Gleiswechselbetrieb (Zug fährt auf dem Gegengleis)", "bild": _tafel_signal(label="→", bg="#f5f0ec")},
    {"code": "Zs2", "frage": "Was bedeutet das Zusatzsignal Zs2 mit Kennbuchstabe?", "antwort": "Ersatzsignal (wie Zs1), aber ferngesteuert mit Kennbuchstabe angezeigt", "bild": _tafel_signal(label="K")},
    {"code": "Sh2", "frage": "Wofür steht das Rangier-Ersatzsignal Sh2?", "antwort": "Erlaubt Rangierfahrten die Weiterfahrt, obwohl Sh0 (Halt) angezeigt wird", "bild": _tafel_signal(label="Sh2")},
    {"code": "Hl-System", "frage": "Welches Signalsystem nutzte die Deutsche Reichsbahn (DDR) zusätzlich zum Hp-System?", "antwort": "Das Hl-Signalsystem", "bild": _konzept_signal("🚂")},
    {"code": "Ks-System", "frage": "Welches moderne Signalsystem ersetzt zunehmend das klassische Hp/Vr-System?", "antwort": "Das Ks-Signalsystem (Kombinationssignale)", "bild": _konzept_signal("🚦")},
    {"code": "Sv-System", "frage": "Wofür sind Sv-Signale auf Schnellfahrstrecken gedacht?", "antwort": "Zur Geschwindigkeitsführung auf Strecken mit sehr hohen Geschwindigkeiten", "bild": _konzept_signal("💨")},
    {"code": "Zp9", "frage": "Wofür wird das Signal Zp9 vom Zugpersonal verwendet?", "antwort": "Um dem Triebfahrzeugführer die Bereitschaft zur Abfahrt zu melden", "bild": _konzept_signal("🚩")},
    {"code": "Wn-System", "frage": "Wofür stehen Wn-Signale allgemein?", "antwort": "Für Warnsignale, die auf besondere Gefahrenstellen im Streckenbereich hinweisen", "bild": _konzept_signal("⚠️")},
    {"code": "Ro-System", "frage": "Für wen sind Ro-Signale (Rottenwarnsignale) gedacht?", "antwort": "Für Streckenarbeiter - sie warnen vor herannahenden Zügen", "bild": _konzept_signal("👷")},
    {"code": "Fz-System", "frage": "Worauf beziehen sich Fz-Signale?", "antwort": "Auf besondere Signale und Kennzeichen an Fahrzeugen selbst", "bild": _konzept_signal("🚃")},
    {"code": "Ts-System", "frage": "Wofür stehen Ts-Signale im Signalbuch?", "antwort": "Für besondere technische Signale, die den Zugbetrieb ergänzend absichern", "bild": _konzept_signal("🔧")},
    {"code": "Orientierungszeichen", "frage": "Wozu dienen Orientierungszeichen entlang der Strecke?", "antwort": "Sie helfen dem Personal bei der Streckenkenntnis, z.B. Kilometrierung oder Kennzeichnung von Anlagen", "bild": _konzept_signal("📍")},
    {"code": "Hebelgewichte", "frage": "Wofür werden Hebelgewichte an Weichen eingesetzt?", "antwort": "Um die Stellung einer Weiche von Hand zu sichern und anzuzeigen", "bild": _konzept_signal("⚙️")},
]

POOLS = {"leicht": LEICHT, "mittel": MITTEL, "schwer": SCHWER}

# Punkte-Multiplikator je Schwierigkeitsgrad (schwerer = mehr Punkte pro Frage)
MULTIPLIKATOR = {"leicht": 1, "mittel": 2, "schwer": 3}

FRAGEN_PRO_RUNDE = 10


def baue_fragen(schwierigkeit):
    """
    Baut FRAGEN_PRO_RUNDE zufällige Fragen für die gewählte Schwierigkeit,
    jede mit 4 Antwortmöglichkeiten (1 richtig + 3 falsche aus demselben
    Schwierigkeitsgrad), fertig gemischt.
    """
    pool = POOLS.get(schwierigkeit, LEICHT)
    anzahl = min(FRAGEN_PRO_RUNDE, len(pool))
    ausgewaehlt = random.sample(pool, anzahl)

    alle_antworten = [item["antwort"] for item in pool]

    fragen = []
    for item in ausgewaehlt:
        falsche = [a for a in alle_antworten if a != item["antwort"]]
        distractoren = random.sample(falsche, min(3, len(falsche)))
        optionen = distractoren + [item["antwort"]]
        random.shuffle(optionen)
        fragen.append(
            {
                "code": item["code"],
                "frage": item["frage"],
                "bild": item["bild"],
                "optionen": optionen,
                "richtig": item["antwort"],
            }
        )
    return fragen
