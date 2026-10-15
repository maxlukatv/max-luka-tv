document.addEventListener("DOMContentLoaded", function() {
    // Prüfen ob ein manuelles Vorschau-Datum gesetzt ist (für dich zum Testen!)
    const urlParams = new URLSearchParams(window.location.search);
    const vorschauDatumStr = urlParams.get('datum'); // Format: YYYY-MM-DD
    const vorschauUhrzeitStr = urlParams.get('uhrzeit'); // Format: HH:MM

    let heute = new Date();
    if (vorschauDatumStr) {
        heute = new Date(vorschauDatumStr + (vorschauUhrzeitStr ? 'T' + vorschauUhrzeitStr : 'T12:00:00'));
    }

    const monat = heute.getMonth() + 1; // 1-12
    const tag = heute.getDate();
    const stunde = heute.getHours();
    const jahr = heute.getFullYear();

    const layer = document.createElement('div');
    layer.id = 'saison-layer';
    document.body.appendChild(layer);

    // Hilfsfunktion für Ostern (grobe Schätzung oder fester Bereich Karfreitag bis Ostermontag)
    // Für dieses Jahr 2026 ist Ostersonntag der 5. April. Karfreitag = 3. April, Ostermontag = 6. April.
    // Wir prüfen hier den Zeitraum 03.04. bis 06.04.2026 (kann flexibel angepasst werden).
    const isDark = document.body.classList.contains('dark-mode') || window.matchMedia('(prefers-color-scheme: dark)').matches;

    // --- 1. OSTEREN (Beispiel für 2026: 03.04. - 06.04.) ---
    if ((monat === 4 && tag >= 3 && tag <= 6) || urlParams.get('modus') === 'ostern') {
        layer.innerHTML = `
            <div style="position:absolute; bottom:0; width:100%; height:40px; background: #2e8b57; border-top: 4px solid #228b22;"></div>
            <div class="hase">🐰</div>
            <div class="osterei" style="left: 15%;">🥚</div>
            <div class="osterei" style="left: 45%; bottom: 5px;">🎨</div>
            <div class="osterei" style="left: 75%;">🥚</div>
        `;
    }

    // --- 2. HALLOWEEN (28.10. bis 01.11.) ---
    else if ((monat === 10 && tag >= 28) || (monat === 11 && tag === 1) || urlParams.get('modus') === 'halloween') {
        layer.innerHTML = `
            <div class="hexe">🧹🧙‍♀️</div>
            <div style="position:absolute; bottom:10px; left:10%; font-size:35px;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:absolute; bottom:10px; right:15%; font-size:40px;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:absolute; top:20px; right:10%; font-size:30px;">🕸️</div>
        `;
        // Wenn Lightmode, lass den Dark/Light-Schalter blinken
        if (!isDark) {
            const themeBtn = document.querySelector('#theme-toggle') || document.querySelector('.theme-switcher');
            if(themeBtn) themeBtn.style.animation = 'blink 1s infinite';
        }
    }

    // --- 3. TOTENSONNTAG BIS NEUJAHR (Ende Nov bis 01.01.) ---
    else if ((monat === 12 && tag >= 1) || (monat === 1 && tag === 1) || urlParams.get('modus') === 'weihnachten') {
        // Schneeflocken erzeugen
        for(let i=0; i<30; i++) {
            letflocke = document.createElement('div');
            letflocke.className = 'schneeflocke';
            letflocke.style.left = Math.random() * 100 + 'vw';
            letflocke.style.width = (Math.random() * 6 + 4) + 'px';
            letflocke.style.height = letflocke.style.width;
            letflocke.style.opacity = Math.random();
            letflocke.style.animationDuration = (Math.random() * 5 + 3) + 's';
            letflocke.style.animationDelay = (Math.random() * 5) + 's';
            layer.appendChild(letflocke);
        }

        // Weihnachtsmann/Engel Flug ab und zu
        layer.innerHTML += `<div class="schlitten">🎅🛷</div>`;

        // Adventskalender & Adventskranz Logik (1. bis 24. Dezember)
        if (monat === 12 && tag <= 24) {
            let kerzenAn = 0;
            if (tag >= 1 && tag < 7) kerzenAn = 1;
            else if (tag >= 7 && tag < 14) kerzenAn = 2;
            else if (tag >= 14 && tag < 21) kerzenAn = 3;
            else if (tag >= 21) kerzenAn = 4;

            console.log(`Adventskranz: ${kerzenAn} Kerzen brennen.`);
        }

        // Geschenke unter dem Baum am 24. Dezember
        if (monat === 12 && tag === 24) {
            const geschenkeDiv = document.createElement('div');
            geschenkeDiv.style.position = 'absolute';
            geschenkeDiv.style.bottom = '15px';
            geschenkeDiv.style.right = '50px';
            geschenkeDiv.style.fontSize = '30px';
            geschenkeDiv.innerHTML = '🎁 📦 🎀';
            layer.appendChild(geschenkeDiv);
        }

        // --- 4. SILVESTER / NEUJAHR (30.12. bis 01.01.) ---
        if ((monat === 12 && tag >= 30) || (monat === 1 && tag === 1) || urlParams.get('modus') === 'silvester') {
            // Automatische Tag/Nacht Umschaltung per Uhrzeit erzwingen (Deaktivieren des manuellen Schalters)
            if (stunde < 7 || stunde >= 19) {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }

            // Countdown bis Neujahr anzeigen
            const silvesterBanner = document.createElement('div');
            silvesterBanner.id = 'silvester-banner';
            document.body.appendChild(silvesterBanner);

            function updateCountdown() {
                const now = new Date();
                const silvester = new Date(jahr, 11, 31, 23, 59, 59);
                const diff = silvester - now;
                if (diff > 0) {
                    const stunden = Math.floor((diff / (1000 * 60 * 60)) % 24);
                    const minuten = Math.floor((diff / 1000 / 60) % 60);
                    const sekunden = Math.floor((diff / 1000) % 60);
                    silvesterBanner.innerHTML = `🎆 Neujahrs-Countdown: ${stunden}h ${minuten}m ${sekunden}s`;
                } else {
                    silvesterBanner.innerHTML = `🎉 Frohes Neues Jahr ${jahr + 1}! 🎇`;
                }
            }
            setInterval(updateCountdown, 1000);
            updateCountdown();

            // Feuerwerk 4 Stunden vor / nach Neujahr
            if (tag === 31 && stunde >= 20 || tag === 1 && stunde <= 4) {
                setInterval(() => {
                    const funke = document.createElement('div');
                    funke.className = 'feuerwerk-funke';
                    funke.style.left = Math.random() * 90 + 5 + 'vw';
                    funke.style.top = Math.random() * 60 + 10 + 'vh';
                    funke.style.backgroundColor = ['#ff0000', '#ffd700', '#00ff00', '#00ffff', '#ff00ff'][Math.floor(Math.random()*5)];
                    layer.appendChild(funke);
                    setTimeout(() => funke.remove(), 1000);
                }, 400);
            }
        }
    }
});