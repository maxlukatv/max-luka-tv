document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    let aktuellerModus = urlParams.get('modus');

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
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    const layer = document.createElement('div');
    layer.id = 'saison-layer';
    document.body.appendChild(layer);

    // Automatische Datums-Erkennung (falls kein manueller Modus gewählt ist)
    if (!aktuellerModus) {
        // Ostern (Karfreitag bis Ostermontag)
        if (monat === 4 && tag >= 3 && tag <= 6) aktuellerModus = 'ostern';
        // Halloween (28.10. bis 01.11.)
        else if ((monat === 10 && tag >= 28) || (monat === 11 && tag === 1)) aktuellerModus = 'halloween';
        // Weihnachten / Winter (Totensonntag/Ende Nov bis 01.01.)
        else if ((monat === 12 && tag >= 1) || (monat === 1 && tag === 1)) aktuellerModus = 'weihnachten';
        // Silvester / Neujahr (30.12. bis 01.01.)
        else if (monat === 12 && tag >= 30 || (monat === 1 && tag <= 1)) aktuellerModus = 'silvester';
    }

    // --- MODI EFFEKTE ---
    if (aktuellerModus === 'ostern') {
        layer.innerHTML = `
            <!-- Grüner Grasboden als wiederholender Balken unten -->
            <div style="position:fixed; bottom:0; left:0; width:100%; height:40px; background: url('/static/img/grassboden.png') repeat-x bottom; background-size: auto 40px; z-index:998; pointer-events:none;"></div>
            
            <!-- Osterei Links -->
            <img src="/static/img/Osterei1.png" alt="Osterei" style="position:fixed; bottom:15px; left:20px; width:110px; height:auto; z-index:998; pointer-events:none;">
            
            <!-- Osterkorb Rechts -->
            <img src="/static/img/Osterkorb.png" alt="Osterkorb" style="position:fixed; bottom:15px; right:150px; width:200px; height:auto; z-index:998; pointer-events:none;">
            
            <!-- Osterei Ganz Rechts -->
            <img src="/static/img/Osterei2.png" alt="Osterei" style="position:fixed; bottom:15px; right:20px; width:110px; height:auto; z-index:998; pointer-events:none;">
        `;
    } 
    else if (aktuellerModus === 'halloween') {
        layer.innerHTML = `
            <div class="hexe">🧹🧙‍♀️</div>
            <div style="position:fixed; bottom:10px; left:10%; font-size:35px; z-index:998;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:fixed; bottom:10px; right:15%; font-size:40px; z-index:998;" class="${isDark ? 'kuerbis-glow' : ''}">🎃</div>
            <div style="position:fixed; top:20px; right:10%; font-size:30px; z-index:998;">🕸️</div>
        `;
    } 
    else if (aktuellerModus === 'weihnachten' || aktuellerModus === 'silvester') {
        for(let i=0; i<30; i++) {
            let flocke = document.createElement('div');
            flocke.className = 'schneeflocke';
            flocke.style.left = Math.random() * 100 + 'vw';
            flocke.style.width = (Math.random() * 6 + 4) + 'px';
            flocke.style.height = flocke.style.width;
            flocke.style.opacity = Math.random();
            flocke.style.animationDuration = (Math.random() * 5 + 3) + 's';
            flocke.style.animationDelay = (Math.random() * 5) + 's';
            layer.appendChild(flocke);
        }
        layer.innerHTML += `<div class="schlitten">🎅🛷</div>`;

        if (monat === 12 && tag === 24) {
            const geschenke = document.createElement('div');
            geschenke.style.cssText = 'position:fixed; bottom:15px; right:50px; font-size:30px; z-index:998;';
            geschenke.innerHTML = '🎁 📦 🎀';
            layer.appendChild(geschenke);
        }

        if (aktuellerModus === 'silvester') {
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

    // --- MANUELLER AUSWAHL-BUTTON UNTEN LINKS (NUR FÜR DICH) ---
    const auswahlBox = document.createElement('div');
    auswahlBox.style.cssText = "position:fixed; bottom:12px; left:12px; background:rgba(20,14,12,0.9); color:white; padding:8px 12px; border-radius:8px; font-size:12px; z-index:10000; display:flex; gap:6px; align-items:center; border: 1px solid var(--border, #3c2f2b); font-family:sans-serif;";
    auswahlBox.innerHTML = `
        <span style="font-weight:bold; margin-right:4px;">Saison:</span>
        <button onclick="setMltvSaison('')" style="background:#444; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">Auto</button>
        <button onclick="setMltvSaison('ostern')" style="background:#2e8b57; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">🐰 Ostern</button>
        <button onclick="setMltvSaison('halloween')" style="background:#ff8c00; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">🎃 Halloween</button>
        <button onclick="setMltvSaison('weihnachten')" style="background:#b22222; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">🎅 Winter</button>
        <button onclick="setMltvSaison('silvester')" style="background:#4682b4; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">🎆 Silvester</button>
    `;
    document.body.appendChild(auswahlBox);
});

function setMltvSaison(modus) {
    try {
        if (!modus) {
            localStorage.removeItem('mltv-saison-modus');
        } else {
            localStorage.setItem('mltv-saison-modus', modus);
        }
    } catch(e) {}
    window.location.href = window.location.pathname + (modus ? '?modus=' + modus : '');
}