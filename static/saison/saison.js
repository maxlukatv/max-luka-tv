document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    let aktuellerModus = urlParams.get('modus');

    // Wenn kein URL-Parameter da ist, prüfen wir den localStorage oder das automatische Datum
    if (!aktuellerModus) {
        try {
            aktuellerModus = localStorage.getItem('mltv-saison-modus');
        } catch (e) {}
    }

    let heute = new Date();
    const monat = heute.getMonth() + 1;
    const tag = heute.getDate();
    const stunde = heute.getHours();
    const jahr = heute.getFullYear();
    const isDark = document.body.classList.contains('dark-mode') || window.matchMedia('(prefers-color-scheme: dark)').matches;

    const layer = document.createElement('div');
    layer.id = 'saison-layer';
    document.body.appendChild(layer);

    // Automatische Erkennung, falls kein manueller Modus gewählt wurde
    if (!aktuellerModus) {
        if (monat === 4 && tag >= 3 && tag <= 6) aktuellerModus = 'ostern';
        else if ((monat === 10 && tag >= 28) || (monat === 11 && tag === 1)) aktuellerModus = 'halloween';
        else if ((monat === 12 && tag >= 1) || (monat === 1 && tag === 1)) aktuellerModus = 'weihnachten';
        else if (monat === 12 && tag >= 30 || (monat === 1 && tag <= 1)) aktuellerModus = 'silvester';
    }

    // --- MODI AUSFÜHREN ---
    if (aktuellerModus === 'ostern') {
        layer.innerHTML = `
            <div style="position:absolute; bottom:0; width:100%; height:40px; background: #2e8b57; border-top: 4px solid #228b22;"></div>
            <div class="hase">🐰</div>
            <div class="osterei" style="left: 15%;">🥚</div>
            <div class="osterei" style="left: 45%; bottom: 5px;">🎨</div>
            <div class="osterei" style="left: 75%;">🥚</div>
        `;
    } 
    else if (aktuellerModus === 'halloween') {
        layer.innerHTML = `
            <div class="hexe">🧹🧙‍♀️</div>
            <div style="position:absolute; bottom:10px; left:10%; font-size:35px;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:absolute; bottom:10px; right:15%; font-size:40px;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:absolute; top:20px; right:10%; font-size:30px;">🕸️</div>
        `;
        if (!isDark) {
            const themeBtn = document.querySelector('#theme-toggle') || document.querySelector('.theme-switcher');
            if(themeBtn) themeBtn.style.animation = 'blink 1s infinite';
        }
    } 
    else if (aktuellerModus === 'weihnachten' || aktuellerModus === 'silvester') {
        for(let i=0; i<30; i++) {
            let letflocke = document.createElement('div');
            letflocke.className = 'schneeflocke';
            letflocke.style.left = Math.random() * 100 + 'vw';
            letflocke.style.width = (Math.random() * 6 + 4) + 'px';
            letflocke.style.height = letflocke.style.width;
            letflocke.style.opacity = Math.random();
            letflocke.style.animationDuration = (Math.random() * 5 + 3) + 's';
            letflocke.style.animationDelay = (Math.random() * 5) + 's';
            layer.appendChild(letflocke);
        }
        layer.innerHTML += `<div class="schlitten">🎅🛷</div>`;

        if (aktuellerModus === 'silvester') {
            if (stunde < 7 || stunde >= 19) {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }

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
                    silvesterBanner.innerHTML = `🎆 Countdown: ${stunden}h ${minuten}m ${sekunden}s`;
                } else {
                    silvesterBanner.innerHTML = `🎉 Frohes Neues Jahr! 🎇`;
                }
            }
            setInterval(updateCountdown, 1000);
            updateCountdown();
        }
    }

    // --- KLEINES AUSWAHL-MENÜ (NUR FÜR DICH / UNTEN RECHTS) ---
    const auswahlBox = document.createElement('div');
    auswahlBox.style.cssText = "position:fixed; bottom:10px; left:10px; background:rgba(0,0,0,0.75); color:white; padding:8px 12px; border-radius:8px; font-size:12px; z-index:10000; display:flex; gap:6px; align-items:center; backdrop-filter:blur(5px); border: 1px solid rgba(255,255,255,0.2);";
    auswahlBox.innerHTML = `
        <span style="font-weight:bold; margin-right:4px;">Saison:</span>
        <button onclick="setSaison('')" style="background:#555; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;">Auto</button>
        <button onclick="setSaison('ostern')" style="background:#2e8b57; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;">Ostern</button>
        <button onclick="setSaison('halloween')" style="background:#ff8c00; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;">Halloween</button>
        <button onclick="setSaison('weihnachten')" style="background:#b22222; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;">Weihnachten</button>
        <button onclick="setSaison('silvester')" style="background:#4682b4; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;">Silvester</button>
    `;
    document.body.appendChild(auswahlBox);
});

function setSaison(modus) {
    try {
        if(modus === '') {
            localStorage.removeItem('mltv-saison-modus');
        } else {
            localStorage.setItem('mltv-saison-modus', modus);
        }
    } catch(e) {}
    window.location.search = modus ? '?modus=' + modus : '';
}