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
    // 1. Schneemann unten links einfügen
    const snowman = document.createElement("div");
    snowman.className = "xmas-snowman";
    snowman.textContent = "⛄";
    snowman.setAttribute("aria-hidden", "true");
    document.body.appendChild(snowman);

    // 2. Schneeflocken-Generator
    const flakes = ["❄", "❅", "❆", "•"];
    function spawnSnowflake() {
      if (document.hidden) return;
      const flake = document.createElement("span");
      flake.className = "xmas-snowflake";
      flake.textContent = flakes[Math.floor(Math.random() * flakes.length)];

      const size = Math.random() * 12 + 10; // 10px bis 22px
      const startLeft = Math.random() * 100; // 0vw bis 100vw
      const duration = Math.random() * 6 + 7; // 7s bis 13s
      const opacity = Math.random() * 0.5 + 0.45;

      flake.style.left = startLeft + "vw";
      flake.style.fontSize = size + "px";
      flake.style.opacity = opacity.toFixed(2);
      flake.style.animationDuration = duration + "s";

      document.body.appendChild(flake);

      setTimeout(() => {
        flake.remove();
      }, duration * 1000 + 200);
    }

    // Alle 450 ms eine neue Schneeflocke
    setInterval(spawnSnowflake, 450);

    // 3. Weihnachtsmann auf Schlitten fliegen lassen
    function spawnSanta() {
      if (document.hidden) return;
      const santa = document.createElement("div");
      santa.className = "xmas-santa";
      santa.setAttribute("aria-hidden", "true");
      santa.innerHTML = '<span class="xmas-santa-inner">🎅🛷🦌🦌</span>';
      document.body.appendChild(santa);

      setTimeout(() => {
        santa.remove();
      }, 14500);
    }

    // Erster Flug 4 Sekunden nach Seitenaufruf, danach alle 45 Sekunden
    setTimeout(spawnSanta, 4000);
    setInterval(spawnSanta, 45000);
  });
})();