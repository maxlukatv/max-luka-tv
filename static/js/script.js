// Sanfte Scroll-Reveal-Animation für News-Karten und Link-Kacheln
document.addEventListener("DOMContentLoaded", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items = document.querySelectorAll(".video-card, .link-card, .news-card");

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    items.forEach((el) => el.style.opacity = 1);
    return;
  }

  items.forEach((el) => {
    el.style.opacity = 0;
    el.style.transform = "translateY(12px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  items.forEach((el) => observer.observe(el));
});

// Hell-/Dunkelmodus-Kettchen: Klick "zieht" das Kettchen und schaltet das
// Farbschema um. Die Wahl wird gespeichert, damit sie auf jeder Unterseite
// erhalten bleibt (das Umschalten selbst ist nur auf der Startseite
// möglich, aber der gewählte Modus gilt für die ganze Webseite).
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".theme-pull");
  if (!toggle) return;

  const knob = toggle.querySelector(".theme-pull-knob");
  const root = document.documentElement;

  function isDarkActive() {
    return root.getAttribute("data-theme") === "dark";
  }

  function updateKnob() {
    const dark = isDarkActive();
    knob.textContent = dark ? "🌙" : "☀️";
    toggle.setAttribute(
      "aria-label",
      dark ? "Zu Hellmodus wechseln" : "Zu Dunkelmodus wechseln"
    );
  }

  updateKnob();

  toggle.addEventListener("click", () => {
    toggle.classList.add("pulling");
    setTimeout(() => toggle.classList.remove("pulling"), 550);

    if (isDarkActive()) {
      root.removeAttribute("data-theme");
      try { localStorage.setItem("mltv-theme", "light"); } catch (e) {}
    } else {
      root.setAttribute("data-theme", "dark");
      try { localStorage.setItem("mltv-theme", "dark"); } catch (e) {}
    }
    updateKnob();
  });
});

/* ==========================================================================
   WEIHNACHTSSTIMMUNG (Aktiv vom 25. November bis 6. Januar)
   ========================================================================== */
(function () {
  const now = new Date();
  const month = now.getMonth(); // 0 = Jan, 10 = Nov, 11 = Dez
  const day = now.getDate();

  // Aktiv ab 25. November bis einschließlich 6. Januar
  const isChristmasSeason =
    (month === 10 && day >= 25) ||
    month === 11 ||
    (month === 0 && day <= 6);

  if (!isChristmasSeason) return;

  document.addEventListener("DOMContentLoaded", () => {
    // Winterlich dunklen, bläulichen Hintergrund aktivieren
    document.body.classList.add("xmas-theme");

    // 1. Größeren Schneemann unten links einfügen
    const snowman = document.createElement("div");
    snowman.className = "xmas-snowman";
    snowman.textContent = "⛄";
    snowman.setAttribute("aria-hidden", "true");
    document.body.appendChild(snowman);

    // 2. Schneeflocken-Generator (größer, kräftiger und etwas dichter)
    const flakes = ["❄", "❅", "❆", "❄", "❅"];
    function spawnSnowflake() {
      if (document.hidden) return;
      const flake = document.createElement("span");
      flake.className = "xmas-snowflake";
      flake.textContent = flakes[Math.floor(Math.random() * flakes.length)];

      const size = Math.random() * 18 + 16; // 16px bis 34px
      const startLeft = Math.random() * 100; // 0vw bis 100vw
      const duration = Math.random() * 5 + 6.5; // 6.5s bis 11.5s
      const opacity = Math.random() * 0.25 + 0.75; // 0.75 bis 1.0 (stark sichtbar)

      flake.style.left = startLeft + "vw";
      flake.style.fontSize = size + "px";
      flake.style.opacity = opacity.toFixed(2);
      flake.style.animationDuration = duration + "s";

      document.body.appendChild(flake);

      setTimeout(() => {
        flake.remove();
      }, duration * 1000 + 200);
    }

    // Alle 320 ms eine neue Schneeflocke
    setInterval(spawnSnowflake, 320);

    // 3. Weihnachtsmann auf Schlitten zu zufälligen Zeiten & Höhen fliegen lassen
    function spawnSanta() {
      if (!document.hidden) {
        const santa = document.createElement("div");
        santa.className = "xmas-santa";
        santa.setAttribute("aria-hidden", "true");

        // Zufällige Flughöhe zwischen 10% und 42% der Bildschirmhöhe
        const randomTop = Math.floor(Math.random() * 32) + 10;
        santa.style.top = randomTop + "vh";

        santa.innerHTML = '<span class="xmas-santa-inner">🎅🛷🦌🦌</span>';
        document.body.appendChild(santa);

        setTimeout(() => {
          santa.remove();
        }, 13500);
      }

      // Nächsten Flug zufällig in 15 bis 55 Sekunden planen
      const nextDelay = Math.floor(Math.random() * 40000) + 15000;
      setTimeout(spawnSanta, nextDelay);
    }

    // Erster Flug zufällig zwischen 3 und 12 Sekunden nach Seitenaufruf
    const initialDelay = Math.floor(Math.random() * 9000) + 3000;
    setTimeout(spawnSanta, initialDelay);
  });
})();