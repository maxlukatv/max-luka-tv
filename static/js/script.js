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
