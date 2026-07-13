document$.subscribe(() => {
  for (const card of document.querySelectorAll(".farm-card")) {
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      card.style.setProperty("--farm-rotate-x", `${(-y * 4).toFixed(2)}deg`);
      card.style.setProperty("--farm-rotate-y", `${(x * 4).toFixed(2)}deg`);
    });

    card.addEventListener("pointerleave", () => {
      card.style.setProperty("--farm-rotate-x", "0deg");
      card.style.setProperty("--farm-rotate-y", "0deg");
    });
  }
});
