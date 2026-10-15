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
    "ra": "Signale für den Rangierdienst (Ra)",
    "el": "Fahrleitungssignale (El)",
    "lf": "Langsamfahrsignale (Lf)",
    "bü": "Bahnübergangssignale (Bü)",
    "hl": "Historische Reichsbahn-Signale (Hl)",
    "sv": "Haupt- und Vorsignalverbindungen (Sv)",
    "ts": "Signale für Schiebelokomotiven und Sperrfahrten (Ts)",
    "wn": "Weichensignale (Wn)",
    "zg": "Zugsignale (Zg)",
    "zp": "Zugpersonal-Signale (Zp)",
    "ro": "Rottenwarnsignale (Ro)",
    "fz": "Fahrzeugsignale (Fz)",
    "so": "Sonstige Signale (So)",
}


def _pfad(kategorie, dateiname):
    def _n(t):
        return t.replace("ü", "ue")

    return f"signale/{_n(kategorie)}/{_n(dateiname)}"


# code, kategorie, bilddatei, sounddatei_oder_None, frage, antwort, im_quiz
_ROH = [
    ("hp0", "hp", "hp0.png", None, "Was bedeutet dieses Signal?", "Halt", True),
    ("hp1", "hp", "hp1.png", None, "Was bedeutet dieses Signal?", "Fahrt", True),
    ("hp2", "hp", "hp2.png", None, "Was bedeutet dieses Signal?", "Langsamfahrt", True),
    ("vr0", "vr", "vr0.png", None, "Was bedeutet dieses Signal?", "Halt erwarten", True),
    ("vr1", "vr", "vr1.png", None, "Was bedeutet dieses Signal?", "Fahr erwarten", True),
    ("vr2", "vr", "vr2.png", None, "Was bedeutet dieses Signal?", "Langsamfahrt erwarten", True),
    ("ks1", "ks", "ks1.png", None, "Was bedeutet dieses Signal?", "Fahrt", True),
    ("ks1-blinken", "ks", "ks1-blinken.gif", None, "Was bedeutet dieses blinkende Signal?", "Fahrt, mit geschwindigkeitsbeschränkung", True),
    ("ks2", "ks", "ks2.png", None, "Was bedeutet dieses Signal?", "Halt erwarten", True),
    ("sh0", "sh", "sh0.png", None, "Was bedeutet dieses Rangiersignal?", "Halt! Fahrverbot", True),
    ("sh1", "sh", "sh1.png", None, "Was bedeutet dieses Rangiersignal?", "Fahrverbot aufgehoben. / Rangierfahrt erlaubt.", True),
    ("sh2", "sh", "sh2.png", None, "Was bedeutet dieses Rangiersignal?", "Schutzhalt", True),
    ("sh3", "sh", "sh3.png", None, "Was bedeutet dieses Rangiersignal?", "Kreissignal", False),
    ("sh5", "sh", "sh5.mp3", "sh5.mp3", "Was bedeutet dieses akustische Signal?", "Horn- und Pfeifsignal", True),
    ("zs1", "zs", "zs1.gif", None, "Was bedeutet dieses Zusatzsignal?", "Ersatzsignal", True),
    ("zs2", "zs", "zs2.png", None, "Was bedeutet dieses Zusatzsignal?", "Richtungsanzeiger", True),
    ("zs2v", "zs", "zs2v.png", None, "Was bedeutet dieses Zusatzsignal?", "Richtungsvoranzeiger", True),
    ("zs3", "zs", "zs3.png", None, "Was bedeutet dieses Zusatzsignal mit einer Zahl?", "Geschwindigkeitsanzeiger", True),
    ("zs3v", "zs", "zs3v.png", None, "Was bedeutet dieses Zusatzsignal?", "Geschwindigkeitsvoranzeiger", True),
    ("zs6", "zs", "zs6.png", None, "Was bedeutet dieses Zusatzsignal?", "Gegengleisanzeiger", True),
    ("zs7", "zs", "zs7.png", None, "Was bedeutet dieses Zusatzsignal?", "Vorsichtsignal", True),
    ("zs8", "zs", "zs8.gif", None, "Was bedeutet dieses Zusatzsignal?", "Gegengleis Ersatzsignal", True),
    ("zs9", "zs", "zs9.png", None, "Was bedeutet dieses Zusatzsignal?", "Bahnübergangstafel", False),
    ("zs10", "zs", "zs10.png", None, "Was bedeutet dieses Zusatzsignal?", "Endesignal", False),
    ("zs103", "zs", "zs103.png", None, "Was bedeutet dieses Zusatzsignal?", "Rautentafel", False),
    ("zs12", "zs", "zs12.png", None, "Was bedeutet dieses Zusatzsignal?", "M-Tafel", True),
    ("zs13", "zs", "zs13.png", None, "Was bedeutet dieses Zusatzsignal?", "Stumpfgleis- und Frühhaltanzeiger", False),
    ("ne1", "ne", "ne1.png", None, "Wofür steht diese Tafel?", "Trapeztafel", True),
    ("ne2", "ne", "ne2.png", None, "Wofür steht diese Tafel?", "Vorsignaltafel", True),
    ("ne3", "ne", "ne3.png", None, "Wofür steht diese Tafel?", "Vorsignalbaken", True),
    ("ne4", "ne", "ne4.png", None, "Wofür steht diese Tafel?", "Schachbretttafel", False),
    ("ne5", "ne", "ne5.png", None, "Wofür steht diese Tafel?", "Haltetafel", True),
    ("ne6", "ne", "ne6.png", None, "Wofür steht diese Tafel?", "Haltepunkttafel", True),
    ("ne7a", "ne", "ne7a.png", None, "Wofür steht diese Tafel?", "Pflugschar heben", False),
    ("ne7b", "ne", "ne7b.png", None, "Wofür steht diese Tafel?", "Pflugschar senken", False),
    ("ne12", "ne", "ne12.png", None, "Wofür steht diese Tafel?", "Ankündigungsbake", False),
    ("ne13a", "ne", "ne13a.png", None, "Wofür steht diese Tafel?", "Die Rückfallweiche ist gegen die Spitze befahrbar.", False),
    ("ne13b", "ne", "ne13b.png", None, "Wofür steht diese Tafel?", "Die Rückfallweiche ist gegen die Spitze nicht befahrbar, vor der Weiche halten.", False),
    ("ne14", "ne", "ne14.png", None, "Wofür steht diese Tafel?", "ETCS-Halt-Tafel (ETCS Stop marker)", False),
    ("ra1", "ra", "ra1.mp3", "ra1.mp3", "Was bedeutet dieses akustische Signal?", "Wegfahren", True),
    ("ra1hand", "ra", "ra1hand.png", None, "Was bedeutet dieses Handzeichen?", "Wegfahren", True),
    ("ra2", "ra", "ra2.mp3", "ra2.mp3", "Was bedeutet dieses akustische Signal?", "Herkommen", False),
    ("ra2hand", "ra", "ra2hand.png", None, "Was bedeutet dieses Handzeichen?", "Herkommen", False),
    ("ra3", "ra", "ra3.mp3", "ra3.mp3", "Was bedeutet dieses akustische Signal?", "Aufdrücken", False),
    ("ra3hand", "ra", "ra3hand.png", None, "Was bedeutet dieses Handzeichen?", "Aufdrücken", False),
    ("ra4", "ra", "ra4.mp3", "ra4.mp3", "Was bedeutet dieses akustische Signal?", "Abstoßen", False),
    ("ra4hand", "ra", "ra4hand.png", None, "Was bedeutet dieses Handzeichen?", "Abstoßen", False),
    ("ra5", "ra", "ra5.mp3", "ra5.mp3", "Was bedeutet dieses akustische Signal?", "Rangierhalt", False),
    ("ra5hand", "ra", "ra5hand.png", None, "Was bedeutet dieses Handzeichen?", "Rangierhalt", False),
    ("ra6", "ra", "ra6.png", None, "Wofür steht diese Tafel?", "Halt! Abdrücken verboten", False),
    ("ra7", "ra", "ra7.png", None, "Wofür steht diese Tafel?", "Langsam abdrücken", False),
    ("ra8", "ra", "ra8.png", None, "Wofür steht diese Tafel?", "Mäßig schnell abdrücken", False),
    ("ra9", "ra", "ra9.png", None, "Wofür steht diese Tafel?", "Zurückziehen", False),
    ("ra10", "ra", "ra10.png", None, "Wofür steht diese Tafel?", "Rangierhalttafel", True),
    ("ra11", "ra", "ra11.png", None, "Wofür steht diese Tafel?", "Wartezeichen", True),
    ("ra12", "ra", "ra12.png", None, "Wofür steht diese Tafel?", "Grenzzeichen", True),
    ("ra13", "ra", "ra13.png", None, "Wofür steht diese Tafel?", "Isolierzeichen", False),
    ("el1", "el", "el1.png", None, "Was bedeutet dieses Signal?", "Ausschaltsignal", True),
    ("el1v", "el", "el1v.png", None, "Was bedeutet dieses Signal?", "Signal El 1 erwarten", True),
    ("el2", "el", "el2.png", None, "Was bedeutet dieses Signal?", "Einschaltsignal", True),
    ("el3", "el", "el3.png", None, "Was bedeutet dieses Signal?", "„Bügel ab“-Ankündigungssignal", True),
    ("el4", "el", "el4.png", None, "Was bedeutet dieses Signal?", "„Bügel ab“ Signal", False),
    ("el5", "el", "el5.png", None, "Was bedeutet dieses Signal?", "„Bügel an“ Signal", False),
    ("el6", "el", "el6.png", None, "Was bedeutet dieses Signal?", "Halt für Fahrzeuge mit gehobenen Stromabnehmern", False),
    ("lf1", "lf", "lf1.png", None, "Was bedeutet dieses Signal?", "Langsamfahrscheibe", True),
    ("lf3", "lf", "lf3.png", None, "Was bedeutet dieses Signal?", "Endscheibe", True),
    ("lf4", "lf", "lf4.png", None, "Was bedeutet dieses Signal?", "Geschwindigkeitstafel", True),
    ("lf4dv", "lf", "lf4dv.png", None, "Was bedeutet dieses Signal?", "Geschwindigkeitstafel", False),
    ("lf5", "lf", "lf5.png", None, "Was bedeutet dieses Signal?", "Anfangstafel", False),
    ("lf6", "lf", "lf6.png", None, "Was bedeutet dieses Signal?", "Geschwindigkeits-Ankündigungssignal", False),
    ("lf7", "lf", "lf7.png", None, "Was bedeutet dieses Signal?", "Geschwindigkeitssignal", False),
    ("lf1/2", "lf", "lf12.png", None, "Was bedeutet dieses Signal?", "Langsamfahrbeginnscheibe", False),
    ("bü0", "bü", "bü0.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Halt vor dem Bahnübergang! Weiterfahrt nach Sicherung.", True),
    ("bü1", "bü", "bü1.gif", None, "Was bedeutet dieses Bahnübergangssignal?", "Der Bahnübergang darf befahren werden.", True),
    ("bü2", "bü", "bü2.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Rautentafel", False),
    ("bü3", "bü", "bü3.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Merktafel", False),
    ("bü4", "bü", "bü4.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Pfeiftafel", False),
    ("bü5", "bü", "bü5.png", None, "Was bedeutet dieses Bahnübergangssignal?", "Läutetafel", False),
    ("hl1", "hl", "hl1.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit Höchstgeschwindigkeit.", True),
    ("hl2", "hl", "hl2.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 100 km/h, dann mit Höchstgeschwindigkeit.", True),
    ("hl3a", "hl", "hl3a.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 40 km/h, dann mit Höchstgeschwindigkeit.", True),
    ("hl3b", "hl", "hl3b.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 60 km/h, dann mit Höchstgeschwindigkeit.", True),
    ("hl4", "hl", "hl4.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Höchstgeschwindigkeit auf 100 km/h ermäßigen.", True),
    ("hl5", "hl", "hl5.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 100 km/h.", True),
    ("hl6a", "hl", "hl6a.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 40 km/h, dann mit 100 km/h.", True),
    ("hl6b", "hl", "hl6b.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 60 km/h, dann mit 100 km/h.", True),
    ("hl7", "hl", "hl7.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Höchstgeschwindigkeit auf 40 km/h (60 km/h) ermäßigen.", False),
    ("hl8", "hl", "hl8.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Geschwindigkeit 100 km/h auf 40 km/h (60 km/h) ermäßigen.", False),
    ("hl9a", "hl", "hl9a.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 40 km/h, dann mit 40 km/h (60 km/h).", False),
    ("hl9b", "hl", "hl9b.gif", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Fahrt mit 60 km/h, dann mit 40 km/h (60 km/h).", False),
    ("hl10", "hl", "hl10.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "„Halt“ erwarten.", False),
    ("hl11", "hl", "hl11.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Geschwindigkeit 100 km/h ermäßigen, „Halt“ erwarten.", False),
    ("hl12a", "hl", "hl12a.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Geschwindigkeit 40 km/h ermäßigen, „Halt“ erwarten.", False),
    ("hl12b", "hl", "hl12b.png", None, "Was bedeutet dieses historische Reichsbahn-Signal?", "Geschwindigkeit 60 km/h ermäßigen, „Halt“ erwarten.", False),
    ("sv0", "sv", "sv0.png", None, "Was bedeutet dieses Signal?", "Zughalt! Weiterfahrt auf Sicht.", True),
    ("sv1", "sv", "sv1.png", None, "Was bedeutet dieses Signal?", "Fahrt! Fahrt erwarten.", True),
    ("sv2", "sv", "sv2.png", None, "Was bedeutet dieses Signal?", "Fahrt! Halt erwarten.", True),
    ("sv3", "sv", "sv3.png", None, "Was bedeutet dieses Signal?", "Fahrt! Langsamfahrt erwarten.", False),
    ("sv4", "sv", "sv4.png", None, "Was bedeutet dieses Signal?", "Langsamfahrt! Fahrt erwarten.", False),
    ("sv5", "sv", "sv5.png", None, "Was bedeutet dieses Signal?", "Langsamfahrt! Langsamfahrt erwarten.", False),
    ("sv6", "sv", "sv6.png", None, "Was bedeutet dieses Signal?", "Langsamfahrt! Halt erwarten.", False),
    ("ts1", "ts", "ts1.png", None, "Was bedeutet dieses Signal?", "Nachschieben einstellen.", False),
    ("ts2", "ts", "ts2.png", None, "Was bedeutet dieses Signal?", "Halt für zurückkehrende Schiebelokomotiven und Sperrfahrten.", False),
    ("ts3", "ts", "ts3.png", None, "Was bedeutet dieses Signal?", "Weiterfahrt für zurückkehrende Schiebelokomotiven und Sperrfahrten.", False),
    ("wn1", "wn", "wn1.png", None, "Was bedeutet dieses Weichensignal?", "Gerader Zweig.", True),
    ("wn2", "wn", "wn2.png", None, "Was bedeutet dieses Weichensignal?", "Gebogener Zweig.", True),
    ("wn3", "wn", "wn3.png", None, "Was bedeutet dieses Weichensignal?", "Gerade von links nach rechts.", False),
    ("wn4", "wn", "wn4.png", None, "Was bedeutet dieses Weichensignal?", "Gerade von rechts nach links.", False),
    ("wn5", "wn", "wn5.png", None, "Was bedeutet dieses Weichensignal?", "Bogen von links nach links.", False),
    ("wn6", "wn", "wn6.png", None, "Was bedeutet dieses Weichensignal?", "Bogen von rechts nach rechts.", False),
    ("wn7", "wn", "wn7.png", None, "Was bedeutet dieses Weichensignal?", "Die Gleissperre ist abgelegt.", False),
    ("zg1", "zg", "zg1.png", None, "Was zeigt dieses Signal am Zug?", "Spitzensignal", True),
    ("zg2lichternacht", "zg", "zg2lichternacht.png", None, "Was zeigt dieses Signal am Zug bei Nacht?", "Schlusssignal", True),
    ("zg2schildernacht", "zg", "zg2schildernacht.png", None, "Was zeigt dieses Signal am Zug bei Nacht?", "Schlusssignal", True),
    ("zp1", "zp", "zp1.mp3", "zp1.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Achtungssignal", True),
    ("zp2", "zp", "zp2.mp3", "zp2.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Handbremse mäßig anziehen.", True),
    ("zp3", "zp", "zp3.mp3", "zp3.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Handbremse stark anziehen.", True),
    ("zp4", "zp", "zp4.mp3", "zp4.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Handbremse lösen.", True),
    ("zp5", "zp", "zp5.mp3", "zp5.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Notsignal", True),
    ("zp6", "zp", "zp6.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Bremse anlegen.", False),
    ("zp7", "zp", "zp7.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Bremse lösen.", False),
    ("zp8", "zp", "zp8.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Bremse in Ordnung.", False),
    ("zp9", "zp", "zp9.png", None, "Was bedeutet dieses Signal des Zugpersonals?", "Abfahren.", True),
    ("zp10", "zp", "zp10.png", None, "Was bedeutet dieses Handzeichen des Zugpersonals?", "Türschließauftrag", False),
    ("zp11", "zp", "zp11.mp3", "zp11.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Kommen", True),
    ("zp12", "zp", "zp12.mp3", "zp12.mp3", "Was bedeutet dieses Signal des Zugpersonals?", "Grenzzeichenfrei", True),
    ("ro1", "ro", "ro1.mp3", "ro1.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Vorsicht! Im Nachbargleis nähern sich Fahrzeuge.", True),
    ("ro2", "ro", "ro2.mp3", "ro2.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Arbeitsgleise räumen.", True),
    ("ro3", "ro", "ro3.mp3", "ro3.mp3", "Was bedeutet dieses Warnsignal für Streckenarbeiter?", "Arbeitsgleise schnellstens räumen.", True),
    ("ro4", "ro", "ro4.png", None, "Wofür steht diese Tafel?", "Fahnenschild", False),
    ("fz1", "fz", "fz1.png", None, "Was zeigt dieses Signal an einem Fahrzeug?", "Rangierlokomotivsignal", True),
    ("fz2", "fz", "fz2.png", None, "Was zeigt dieses Signal an einem Fahrzeug?", "Gelbe Fahne", False),
    ("so1", "so", "so1.png", None, "Was bedeutet dieses Signal?", "Endtafel", False),
    ("so19", "so", "so19.png", None, "Was bedeutet dieses Signal?", "Hauptsignalbaken", False),
    ("so106", "so", "so106.png", None, "Was bedeutet dieses Signal?", "Kreuztafel", False),
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
    """10 zufällige Fragen quer durch alle Kategorien, je 3 Antworten vorrangig aus derselben Kategorie."""
    quiz_pool = [s for s in ALLE_SIGNALE if s["im_quiz"]]
    anzahl = min(FRAGEN_PRO_RUNDE, len(quiz_pool))
    ausgewaehlt = random.sample(quiz_pool, anzahl)

    fragen = []
    for item in ausgewaehlt:
        kategorie = item["kategorie"]
        richtige_antwort = item["antwort"]
        
        # 1. Versuche Antworten aus derselben Kategorie zu holen
        gleiche_kat_antworten = list({
            s["antwort"] for s in quiz_pool 
            if s["kategorie"] == kategorie and s["antwort"] != richtige_antwort
        })
        random.shuffle(gleiche_kat_antworten)
        
        distraktoren = []
        benoetigt = ANTWORTEN_PRO_FRAGE - 1 # Normalerweise 2 falsche Antworten
        
        # 2. Wenn die Kategorie genug eigene Antworten hat, nimm sie
        if len(gleiche_kat_antworten) >= benoetigt:
            distraktoren = gleiche_kat_antworten[:benoetigt]
        else:
            # Ansonsten nimm alle die da sind und fülle den Rest sicher aus dem Gesamtpool auf
            distraktoren = gleiche_kat_antworten.copy()
            rest_kandidaten = list({
                s["antwort"] for s in quiz_pool 
                if s["antwort"] != richtige_antwort and s["antwort"] not in distraktoren
            })
            random.shuffle(rest_kandidaten)
            fehlend = benoetigt - len(distraktoren)
            distraktoren.extend(rest_kandidaten[:fehlend])

        # 3. Optionen zusammenbauen und mischen
        optionen = distraktoren + [richtige_antwort]
        random.shuffle(optionen)
        
        fragen.append(
            {
                "code": item["code"],
                "frage": item["frage"],
                "bild": item["bild"],
                "sound": item["sound"],
                "optionen": optionen,
                "richtig": richtige_antwort,
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
