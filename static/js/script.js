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
