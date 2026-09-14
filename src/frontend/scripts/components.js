document.querySelector(".menu-toggle")?.addEventListener("click", () => document.querySelector(".app-sidebar")?.classList.toggle("is-open"));

document.querySelectorAll("[data-tabs]").forEach((group) => group.addEventListener("click", (event) => {
    const tab = event.target.closest("button[data-target]");
    if (!tab) return;
    group.querySelectorAll("button").forEach((item) => item.classList.toggle("is-active", item === tab));
    document.querySelectorAll("[data-tab-panel]").forEach((panel) => panel.hidden = panel.id !== tab.dataset.target);
}));

document.querySelectorAll("[data-confirm]").forEach((form) => form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
}));
