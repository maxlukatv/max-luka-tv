"""
Datenbank für das Signale-Lernspiel (/signale_lernen).

Hinweis: Hobby-/Lernprojekt für Freizeit und Spaß - KEIN offizielles
Ausbildungsmaterial. Bei selteneren/historischen Signalen sind die
Erklärungen bewusst allgemein gehalten.

im_quiz=True: Signal kommt im Quiz vor. False: nur im Katalog (zu allgemein
oder unsicher für eine faire Quiz-Frage).
"""

import random

KATEGORIE_NAMEN = {
    "hp": "Hauptsignale (Hp)",
    "vr": "Vorsignale (Vr)",
    "ks": "Kombinationssignale (Ks)",
    "sh": "Rangiersignale (Sh)",
    "zs": "Zusatzsignale (Zs)",
    "ne": "Nebensignale (Ne)",
    "ra": "Ankündigungs- und Rangiersignale (Ra)",
    "el": "Elektro-Signale (El)",
    "lf": "Langsamfahrsignale (Lf)",
    "bue": "Bahnübergangssignale (Bü)",
    "hl": "Historische Reichsbahn-Signale (Hl)",
    "sv": "Schnellfahrstrecken-Signale (Sv)",
    "ts": "Technische Signale (Ts)",
    "wn": "Warnsignale (Wn)",
    "zg": "Zugsignale (Zg)",
    "zp": "Zugpersonal-Signale (Zp)",
    "ro": "Rottenwarnsignale (Ro)",
    "fz": "Fahrzeugsignale (Fz)",
    "so": "Sonstige Signale (So)",
}


def _pfad(kategorie, dateiname):
    return f"signale/{kategorie}/{dateiname}"


# code, kategorie, bilddatei, sounddatei_oder_None, frage, antwort, im_quiz
_ROH = [
    ("hp0", "hp", "hp0.png", None, "Was bedeutet dieses Signal?", "Halt! Hier anhalten.", True),
    ("hp1", "hp", "hp1.png", None, "Was bedeutet dieses Signal?", "Fahrt frei - mit voller Geschwindigkeit weiterfahren.", True),
    ("hp2", "hp", "hp2.png", None, "Was bedeutet dieses Signal?", "Fahrt frei - aber nur langsam weiterfahren.", True),
    ("vr0", "vr", "vr0.png", None, "Was bedeutet dieses Signal?", "Achtung: Das nächste Signal zeigt bald Halt.", True),
    ("vr1", "vr", "vr1.png", None, "Was bedeutet dieses Signal?", "Das nächste Signal zeigt bald Fahrt frei.", True),
    ("vr2", "vr", "vr2.png", None, "Was bedeutet dieses Signal?", "Das nächste Signal zeigt bald eine Langsamfahrt.", True),
    ("ks1", "ks", "ks1.png", None, "Was bedeutet dieses Signal?", "Fahrt frei.", True),
    ("ks1-blinken", "ks", "ks1-blinken.gif", None, "Was bedeutet dieses blinkende Signal?", "Fahrt frei - aber das nächste Signal zeigt bald Halt.", True),
    ("ks2", "ks", "ks2.png", None, "Was bedeutet dieses Signal?", "Fahrt frei - aber nur langsam weiterfahren.", True),
    ("sh0", "sh", "sh0.png", None, "Was bedeutet dieses Rangiersignal?", "Halt für Rangierfahrten.", True),
    ("sh1", "sh", "sh1.png", None, "Was bedeutet dieses Rangiersignal?", "Die Rangierfahrt darf losfahren.", True),
    ("sh2", "sh", "sh2.png", None, "Was bedeutet dieses Rangiersignal?", "Ersatzsignal - die Rangierfahrt darf trotzdem weiterfahren.", True),
    ("sh3", "sh", "sh3.png", None, "Was bedeutet dieses Rangiersignal?", "Ein besonderes Signal für Rangierfahrten.", False),
    ("sh5", "sh", "sh5.mp3", "sh5.mp3", "Was bedeutet dieses akustische Signal?", "Achtungssignal bei Rangierfahrten (Hupe).", True),
    ("zs1", "zs", "zs1.gif", None, "Was bedeutet dieses Zusatzsignal?", "Ersatzsignal - Weiterfahrt trotz Halt erlaubt.", True),
    ("zs2", "zs", "zs2.png", None, "Was bedeutet dieses Zusatzsignal?", "Ersatzsignal mit Kennbuchstabe (ferngesteuert).", True),
    ("zs2v", "zs", "zs2v.png", None, "Was bedeutet dieses Zusatzsignal?", "Kündigt das Signal Zs2 schon vorher an.", True),
    ("zs3", "zs", "zs3.png", None, "Was bedeutet dieses Zusatzsignal mit einer Zahl?", "Zeigt die erlaubte Geschwindigkeit an (Zahl mal 10 km/h).", True),
    ("zs3v", "zs", "zs3v.png", None, "Was bedeutet dieses Zusatzsignal?", "Kündigt die Geschwindigkeitsbegrenzung schon vorher an.", True),
    ("zs6", "zs", "zs6.png", None, "Was bedeutet dieses Zusatzsignal?", "Rangierfahrt erlaubt, obwohl das Signal Halt zeigt.", True),
    ("zs7", "zs", "zs7.png", None, "Was bedeutet dieses Zusatzsignal?", "Ganz vorsichtig und langsam weiterfahren erlaubt.", True),
    ("zs8", "zs", "zs8.gif", None, "Was bedeutet dieses Zusatzsignal?", "Weiterfahrt nach schriftlichem Befehl erlaubt.", True),
    ("zs9", "zs", "zs9.png", None, "Was bedeutet dieses Zusatzsignal?", "Ein besonderes Zusatzsignal mit eigener Fahrerlaubnis.", False),
    ("zs10", "zs", "zs10.png", None, "Was bedeutet dieses Zusatzsignal?", "Ein zusätzliches Signal mit besonderer Bedeutung.", False),
    ("zs103", "zs", "zs103.png", None, "Was bedeutet dieses Zusatzsignal?", "Ein selten genutztes Zusatzsignal.", False),
    ("zs12", "zs", "zs12.png", None, "Was bedeutet dieses Zusatzsignal?", "Weiterfahrt nach mündlicher Erlaubnis erlaubt.", True),
    ("zs13", "zs", "zs13.png", None, "Was bedeutet dieses Zusatzsignal?", "Ein besonderes Zusatzsignal.", False),
    ("ne1", "ne", "ne1.png", None, "Wofür steht diese Tafel?", "Zeigt ein schwer erkennbares Hauptsignal an.", True),
    ("ne2", "ne", "ne2.png", None, "Wofür steht diese Tafel?", "Zeigt die Stelle, an der ohne Signal gehalten werden muss.", True),
    ("ne3", "ne", "ne3.png", None, "Wofür steht diese Tafel?", "Kündigt ein Vorsignal an.", True),
    ("ne4", "ne", "ne4.png", None, "Wofür steht diese Tafel?", "Kennzeichnet eine bestimmte Stelle auf der Strecke.", False),
    ("ne5", "ne", "ne5.png", None, "Wofür steht diese Tafel?", "Kündigt eine Schutzstrecke an - Vorsicht bei Elektrik.", True),
    ("ne6", "ne", "ne6.png", None, "Wofür steht diese Tafel?", "Zeigt an, dass der Zug auf dem Gegengleis fährt.", True),
    ("ne7a", "ne", "ne7a.png", None, "Wofür steht diese Tafel?", "Ein Kennzeichen für Gleise oder Fahrzeuge.", False),
    ("ne7b", "ne", "ne7b.png", None, "Wofür steht diese Tafel?", "Ein Kennzeichen für Gleise oder Fahrzeuge (Variante).", False),
    ("ne12", "ne", "ne12.png", None, "Wofür steht diese Tafel?", "Ein besonderes Kennzeichen entlang der Strecke.", False),
    ("ne13a", "ne", "ne13a.png", None, "Wofür steht diese Tafel?", "Grenzzeichen - zeigt, wo zwei Gleise sich zu nahekommen.", False),
    ("ne13b", "ne", "ne13b.png", None, "Wofür steht diese Tafel?", "Grenzzeichen - zeigt, wo zwei Gleise sich zu nahekommen (Variante).", False),
    ("ne14", "ne", "ne14.png", None, "Wofür steht diese Tafel?", "Kennzeichnet Anfang oder Ende eines Streckenabschnitts.", False),
    ("ra1", "ra", "ra1.mp3", "ra1.mp3", "Was bedeutet dieses akustische Signal?", "Achtungssignal - hier muss gepfiffen werden.", True),
    ("ra1hand", "ra", "ra1hand.png", None, "Was bedeutet dieses Handzeichen?", "Handzeichen für das Achtungssignal (Pfeifen).", True),
    ("ra2", "ra", "ra2.mp3", "ra2.mp3", "Was bedeutet dieses akustische Signal?", "Ein weiteres akustisches Warnsignal.", False),
    ("ra2hand", "ra", "ra2hand.png", None, "Was bedeutet dieses Handzeichen?", "Handzeichen für dieses Warnsignal.", False),
    ("ra3", "ra", "ra3.mp3", "ra3.mp3", "Was bedeutet dieses akustische Signal?", "Noch ein akustisches Warnsignal.", False),
    ("ra3hand", "ra", "ra3hand.png", None, "Was bedeutet dieses Handzeichen?", "Handzeichen für dieses Warnsignal.", False),
    ("ra4", "ra", "ra4.mp3", "ra4.mp3", "Was bedeutet dieses akustische Signal?", "Ein anderes akustisches Warnsignal.", False),
    ("ra4hand", "ra", "ra4hand.png", None, "Was bedeutet dieses Handzeichen?", "Handzeichen für dieses Warnsignal.", False),
    ("ra5", "ra", "ra5.mp3", "ra5.mp3", "Was bedeutet dieses akustische Signal?", "Ein weiteres Signal mit Ton.", False),
    ("ra5hand", "ra", "ra5hand.png", None, "Was bedeutet dieses Handzeichen?", "Handzeichen für dieses Warnsignal.", False),
    ("ra6", "ra", "ra6.png", None, "Wofür steht diese Tafel?", "Eine Tafel mit besonderer Streckeninformation.", False),
    ("ra7", "ra", "ra7.png", None, "Wofür steht diese Tafel?", "Eine Tafel mit besonderer Streckeninformation.", False),
    ("ra8", "ra", "ra8.png", None, "Wofür steht diese Tafel?", "Eine Tafel mit besonderer Streckeninformation.", False),
    ("ra9", "ra", "ra9.png", None, "Wofür steht diese Tafel?", "Eine Tafel mit besonderer Streckeninformation.", False),
    ("ra10", "ra", "ra10.png", None, "Wofür steht diese Tafel?", "Hier muss gepfiffen werden (Pfeifentafel).", True),
    ("ra11", "ra", "ra11.png", None, "Wofür steht diese Tafel?", "Kündigt eine vorübergehende Langsamfahrstelle an.", True),
    ("ra12", "ra", "ra12.png", None, "Wofür steht diese Tafel?", "Zeigt einen Bahnübergang mit Läutesignal an.", True),
    ("ra13", "ra", "ra13.png", None, "Wofür steht diese Tafel?", "Eine besondere Streckentafel.", False),
    ("el1", "el", "el1.png", None, "Was bedeutet dieses Signal?", "Bald kommt ein Streckenabschnitt ohne Fahrdraht.", True),
    ("el1v", "el", "el1v.png", None, "Was bedeutet dieses Signal?", "Kündigt das Signal El1 schon früher an.", True),
    ("el2", "el", "el2.png", None, "Was bedeutet dieses Signal?", "Hier beginnt der Abschnitt ohne Fahrdraht - Stromabnehmer senken.", True),
    ("el3", "el", "el3.png", None, "Was bedeutet dieses Signal?", "Hier endet der Abschnitt ohne Fahrdraht - Stromabnehmer darf wieder hoch.", True),
    ("el4", "el", "el4.png", None, "Was bedeutet dieses Signal?", "Ähnlich wie El3, mit leicht anderer Bedeutung.", False),
    ("el5", "el", "el5.png", None, "Was bedeutet dieses Signal?", "Ein besonderes Signal für die Oberleitung.", False),
    ("el6", "el", "el6.png", None, "Was bedeutet dieses Signal?", "Ein weiteres Signal für die Oberleitung.", False),
    ("lf1", "lf", "lf1.png", None, "Was bedeutet dieses Signal?", "Zeigt den Anfang einer Langsamfahrstelle.", True),
    ("lf3", "lf", "lf3.png", None, "Was bedeutet dieses Signal?", "Zeigt das Ende einer Langsamfahrstelle.", True),
    ("lf4", "lf", "lf4.png", None, "Was bedeutet dieses Signal?", "Kündigt eine Langsamfahrstelle an.", True),
    ("lf4dv", "lf", "lf4dv.png", None, "Was bedeutet dieses Signal?", "Kündigt eine Langsamfahrstelle an (Variante).", False),
    ("lf5", "lf", "lf5.png", None, "Was bedeutet dieses Signal?", "Ein zusätzliches Signal zur Langsamfahrstelle.", False),
    ("lf6", "lf", "lf6.png", None, "Was bedeutet dieses Signal?", "Ein weiteres Signal zur Langsamfahrstelle.", False),
    ("lf7", "lf", "lf7.png", None, "Was bedeutet dieses Signal?", "Noch ein Signal zur Langsamfahrstelle.", False),
    ("lf12", "lf", "lf12.png", None, "Was bedeutet dieses Signal?", "Ein besonderes Signal rund um Langsamfahrstellen.", False),
    ("bue0", "bue", "bue0.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Zeigt einen ungesicherten Bahnübergang an.", True),
    ("bue1", "bue", "bue1.gif", None, "Was bedeutet dieses Bahnübergangssignal?", "Bahnübergang mit Blinklicht - Achtung.", True),
    ("bue2", "bue", "bue2.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Ein besonderes Signal an einem Bahnübergang.", False),
    ("bue3", "bue", "bue3.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Ein weiteres Signal an einem Bahnübergang.", False),
    ("bue4", "bue", "bue4.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Noch ein Signal an einem Bahnübergang.", False),
    ("bue5", "bue", "bue5.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Ein anderes Signal an einem Bahnübergang.", False),
    ("hl1", "hl", "hl1.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Halt! (historisches Signal der Reichsbahn)", True),
    ("hl2", "hl", "hl2.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt frei (historisches Signal der Reichsbahn)", True),
    ("hl3a", "hl", "hl3a.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Langsamfahrt (historisches Signal der Reichsbahn)", True),
    ("hl3b", "hl", "hl3b.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Langsamfahrt, andere Bauform (historisches Signal)", True),
    ("hl4", "hl", "hl4.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Halt erwarten (historisches Vorsignal der Reichsbahn)", True),
    ("hl5", "hl", "hl5.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt erwarten (historisches Vorsignal der Reichsbahn)", True),
    ("hl6a", "hl", "hl6a.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Langsamfahrt erwarten (historisches Vorsignal der Reichsbahn)", True),
    ("hl6b", "hl", "hl6b.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Langsamfahrt erwarten, andere Bauform (historisches Signal)", True),
    ("hl7", "hl", "hl7.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein weiteres historisches Signal der Reichsbahn.", False),
    ("hl8", "hl", "hl8.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Noch ein historisches Signal der Reichsbahn.", False),
    ("hl9a", "hl", "hl9a.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein anderes historisches Signal der Reichsbahn.", False),
    ("hl9b", "hl", "hl9b.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein historisches Signal der Reichsbahn (Variante).", False),
    ("hl10", "hl", "hl10.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein weiteres Signal der Reichsbahn von früher.", False),
    ("hl11", "hl", "hl11.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Noch ein Signal der Reichsbahn von früher.", False),
    ("hl12a", "hl", "hl12a.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein altes Signal der Reichsbahn.", False),
    ("hl12b", "hl", "hl12b.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Ein altes Signal der Reichsbahn (Variante).", False),
    ("sv0", "sv", "sv0.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Halt.", True),
    ("sv1", "sv", "sv1.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Fahrt frei.", True),
    ("sv2", "sv", "sv2.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Geschwindigkeit beachten.", True),
    ("sv3", "sv", "sv3.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Ein weiteres Signal für Schnellfahrstrecken.", False),
    ("sv4", "sv", "sv4.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Noch ein Signal für Schnellfahrstrecken.", False),
    ("sv5", "sv", "sv5.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Ein anderes Signal für Schnellfahrstrecken.", False),
    ("sv6", "sv", "sv6.png", None, "Was bedeutet dieses Signal auf Schnellfahrstrecken?", "Ein besonderes Signal für Schnellfahrstrecken.", False),
    ("ts1", "ts", "ts1.png", None, "Wofür steht dieses technische Signal?", "Zur technischen Sicherung der Strecke.", False),
    ("ts2", "ts", "ts2.png", None, "Wofür steht dieses technische Signal?", "Ein weiteres technisches Signal zur Streckensicherung.", False),
    ("ts3", "ts", "ts3.png", None, "Wofür steht dieses technische Signal?", "Noch ein technisches Signal zur Streckensicherung.", False),
    ("wn1", "wn", "wn1.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor Gleisarbeiten auf der Strecke.", True),
    ("wn2", "wn", "wn2.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor einer Engstelle am Gleis.", True),
    ("wn3", "wn", "wn3.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor eingeschränkter Sicht.", False),
    ("wn4", "wn", "wn4.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor einer besonderen Gefahrenstelle.", False),
    ("wn5", "wn", "wn5.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor Bauarbeiten in Gleisnähe.", False),
    ("wn6", "wn", "wn6.png", None, "Wofür steht dieses Warnsignal?", "Warnt vor eingeschränktem Lichtraum.", False),
    ("wn7", "wn", "wn7.png", None, "Wofür steht dieses Warnsignal?", "Ein allgemeines Warnsignal für Gefahrenstellen.", False),
    ("zg1", "zg", "zg1.png", None, "Was zeigt dieses Signal am Zug?", "Das Spitzensignal - zeigt die Spitze (vorne) des Zuges.", True),
    ("zg2lichternacht", "zg", "zg2lichternacht.png", None, "Was zeigt dieses Signal am Zug bei Nacht?", "Das Schlusssignal - zeigt das Ende des Zuges.", True),
    ("zg2schildernacht", "zg", "zg2schildernacht.png", None, "Was zeigt dieses Signal am Zug bei Nacht?", "Das Schlusssignal mit Schildern - zeigt das Ende des Zuges.", True),
    ("zp1", "zp", "zp1.mp3", "zp1.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Achtung geben.", True),
    ("zp2", "zp", "zp2.mp3", "zp2.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Bremsen.", True),
    ("zp3", "zp", "zp3.mp3", "zp3.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Langsamer fahren.", True),
    ("zp4", "zp", "zp4.mp3", "zp4.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Halt.", True),
    ("zp5", "zp", "zp5.mp3", "zp5.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Türen schließen.", True),
    ("zp6", "zp", "zp6.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Achtung geben (Handzeichen).", False),
    ("zp7", "zp", "zp7.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Bremsen (Handzeichen).", False),
    ("zp8", "zp", "zp8.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Langsamer fahren (Handzeichen).", False),
    ("zp9", "zp", "zp9.png", None, "Was bedeutet dieses Signal des Zugpersonals?", "Bereit zur Abfahrt - der Fahrtwunsch.", True),
    ("zp10", "zp", "zp10.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Halt (Handzeichen).", False),
    ("zp11", "zp", "zp11.mp3", "zp11.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Abfahrbereit.", True),
    ("zp12", "zp", "zp12.mp3", "zp12.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Ein Notsignal.", True),
    ("ro1", "ro", "ro1.mp3", "ro1.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Ein Zug nähert sich.", True),
    ("ro2", "ro", "ro2.mp3", "ro2.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Der Zug ist ganz nah - sofort Gleis freimachen!", True),
    ("ro3", "ro", "ro3.mp3", "ro3.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Entwarnung - das Gleis ist wieder frei.", True),
    ("ro4", "ro", "ro4.png", None, "Wofür steht diese Tafel?", "Zur Warnung von Streckenarbeitern.", False),
    ("fz1", "fz", "fz1.png", None, "Was zeigt dieses Signal an einem Fahrzeug?", "Ein Kennzeichen an einem Schienenfahrzeug.", True),
    ("fz2", "fz", "fz2.png", None, "Was zeigt dieses Signal an einem Fahrzeug?", "Ein Kennzeichen an einem Schienenfahrzeug (Variante).", False),
    ("so1", "so", "so1.png", None, "Wofür steht dieses Signal?", "Ein sonstiges Signal mit besonderer Bedeutung.", False),
    ("so19", "so", "so19.png", None, "Wofür steht dieses Signal?", "Ein weiteres sonstiges Signal.", False),
    ("so106", "so", "so106.png", None, "Wofür steht dieses Signal?", "Noch ein sonstiges Signal.", False),
]

ALLE_SIGNALE = []
for code, kategorie, dateiname, sound_datei, frage, antwort, im_quiz in _ROH:
    ALLE_SIGNALE.append(
        {
            "code": code,
            "kategorie": kategorie,
            "kategorie_name": KATEGORIE_NAMEN.get(kategorie, kategorie.upper()),
            "bild": _pfad(kategorie, dateiname),
            "sound": _pfad(kategorie, sound_datei) if sound_datei else None,
            "frage": frage,
            "antwort": antwort,
            "im_quiz": im_quiz,
        }
    )

FRAGEN_PRO_RUNDE = 10
ANTWORTEN_PRO_FRAGE = 3
SOUND_MAX_ABSPIELEN = 3


def baue_fragen():
    """10 zufällige Fragen aus allen quiz-tauglichen Signalen, je 3 Antworten."""
    quiz_pool = [s for s in ALLE_SIGNALE if s["im_quiz"]]
    anzahl = min(FRAGEN_PRO_RUNDE, len(quiz_pool))
    ausgewaehlt = random.sample(quiz_pool, anzahl)
    alle_antworten = list({s["antwort"] for s in quiz_pool})

    fragen = []
    for item in ausgewaehlt:
        kandidaten = [a for a in alle_antworten if a != item["antwort"]]
        distraktoren = random.sample(kandidaten, min(ANTWORTEN_PRO_FRAGE - 1, len(kandidaten)))
        optionen = distraktoren + [item["antwort"]]
        random.shuffle(optionen)
        fragen.append(
            {
                "code": item["code"],
                "frage": item["frage"],
                "bild": item["bild"],
                "sound": item["sound"],
                "optionen": optionen,
                "richtig": item["antwort"],
            }
        )
    return fragen


def baue_katalog():
    """Alle Signale gruppiert nach Kategorie, zum Nachschauen ohne Quiz."""
    gruppen = {}
    for item in ALLE_SIGNALE:
        gruppen.setdefault(item["kategorie"], {"name": item["kategorie_name"], "signale": []})
        gruppen[item["kategorie"]]["signale"].append(
            {
                "code": item["code"],
                "bild": item["bild"],
                "sound": item["sound"],
                "antwort": item["antwort"],
            }
        )
    return [gruppen[k] for k in KATEGORIE_NAMEN if k in gruppen]
