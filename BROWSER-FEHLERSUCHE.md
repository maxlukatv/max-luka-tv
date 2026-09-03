# Fehlersuche mit den Browser-DevTools (F12)

So öffnest du die DevTools: F12 drücken (oder Rechtsklick auf die Seite →
"Untersuchen"). Oben im DevTools-Fenster auf "Console" klicken, dann die
Befehle unten einzeln einfügen (kopieren, in die Konsole einfügen, Enter).

---

## 1. Kaputte Bilder finden (z.B. Video-Thumbnails, die nicht laden)

```javascript
document.querySelectorAll('img').forEach(img => {
  if (!img.complete || img.naturalWidth === 0) {
    console.warn('Kaputtes Bild:', img.src);
  }
});
console.log('Fertig geprüft.');
```

Erscheint nichts außer "Fertig geprüft." → alle Bilder laden korrekt.

---

## 2. Alle Links auf der Seite auf Gültigkeit prüfen

```javascript
const links = [...document.querySelectorAll('a[href]')];
console.log(`${links.length} Links gefunden. Prüfe...`);
Promise.all(links.map(a =>
  fetch(a.href, { method: 'HEAD', mode: 'no-cors' })
    .then(() => null)
    .catch(() => a.href)
)).then(results => {
  const broken = results.filter(Boolean);
  if (broken.length) {
    console.warn('Eventuell kaputte Links:', broken);
  } else {
    console.log('Alle Links scheinen erreichbar zu sein.');
  }
});
```

Hinweis: wegen Browser-Sicherheitsregeln (CORS) kann das bei externen
Links (YouTube, Instagram) manchmal einen falschen Alarm zeigen, obwohl
der Link in Wirklichkeit funktioniert. Bei internen Links (deine eigene
Seite) ist das Ergebnis zuverlässig.

---

## 3. JavaScript-Fehler sichtbar machen

Einfach die Seite einmal komplett neu laden (Strg+F5) bei geöffneter
Konsole. Jeder rote Text in der Konsole ist ein JavaScript-Fehler -
schick mir den Text davon, falls etwas auftaucht.

---

## 4. Ladezeit der Seite checken

Im DevTools-Fenster oben auf den Reiter "Network" klicken, dann die
Seite neu laden (Strg+F5). Unten links steht dann z.B. "Finish: 2.3s" -
das ist die Gesamtladezeit. Alles unter 3 Sekunden ist gut.

---

## 5. Mobile Ansicht testen

Im DevTools-Fenster oben links auf das Handy/Tablet-Symbol klicken
(oder Strg+Umschalt+M). Dann oben ein Gerät wie "iPhone 14" auswählen,
um zu sehen, wie deine Seite auf dem Handy aussieht.

---

## 6. Prüfen, ob die Seite HTTPS-sicher lädt (kein "Nicht sicher")

Einfach in der Adresszeile schauen: steht da ein Schloss-Symbol (nicht
"Nicht sicher")? Falls "Nicht sicher" erscheint, sag mir Bescheid -
das würde auf ein Problem mit dem SSL-Zertifikat hindeuten.

---

## Was du mir schicken kannst, wenn etwas komisch aussieht

- Screenshot der Konsole, falls dort roter Text (Fehler) erscheint
- Die Ausgabe von Befehl 1 oder 2, falls dort Warnungen auftauchen
- Einfach eine Beschreibung, was du siehst vs. was du erwartest hättest
