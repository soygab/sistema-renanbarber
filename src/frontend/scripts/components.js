const currentPage = document.body.dataset.page || "";
const currentArea = document.body.dataset.area || "";

let activeSession = null;
try {
    activeSession = JSON.parse(sessionStorage.getItem("renanbarber_session"));
} catch {
    sessionStorage.removeItem("renanbarber_session");
}

if (!activeSession || activeSession.role !== currentArea) {
    window.location.replace("/src/frontend/pages/login.html");
}

const navigation = {
    client: [
        ["cliente-home", "⌂", "Início", "/src/frontend/pages/cliente-home.html"],
        ["meus-agendamentos", "▣", "Meus agendamentos", "/src/frontend/pages/meus-agendamentos.html"],
        ["servicos", "✂", "Serviços", "/src/frontend/pages/servicos.html"],
        ["agendar", "+", "Agendar", "/src/frontend/pages/agendar.html"],
    ],
    barber: [
        ["barbeiro-home", "▦", "Visão geral", "/src/frontend/pages/barbeiro-home.html"],
        ["barbeiro-agendamentos", "▣", "Agenda do dia", "/src/frontend/pages/barbeiro-agendamentos.html"],
        ["barbeiro-servicos", "✂", "Serviços", "/src/frontend/pages/barbeiro-servicos.html"],
        ["barbeiro-horarios", "◷", "Horários", "/src/frontend/pages/barbeiro-horarios.html"],
    ],
};

document.querySelectorAll("[data-sidebar]").forEach((slot) => {
    const area = slot.dataset.sidebar;
    const isClient = area === "client";
    const areaHome = isClient
        ? "/src/frontend/pages/cliente-home.html"
        : "/src/frontend/pages/barbeiro-home.html";
    slot.innerHTML = `
        <aside class="app-sidebar" id="app-sidebar">
            <a class="app-brand" href="${areaHome}">
                <img src="/public/image/logo_renanbarber.svg" alt="">
                <span>Renan<span>Barber</span><small>${isClient ? "Área do cliente" : "Painel da equipe"}</small></span>
            </a>
            <nav class="app-nav" aria-label="${isClient ? "Área do cliente" : "Painel dos barbeiros"}">
                ${navigation[area].map(([id, icon, label, href]) => `
                    <a href="${href}" class="${currentPage === id ? "is-active" : ""}">
                        <i aria-hidden="true">${icon}</i><span>${label}</span>
                    </a>`).join("")}
            </nav>
            <div class="sidebar-profile">
                <span class="avatar">${isClient ? "GS" : "RB"}</span>
                <span>${isClient ? "Gabriel Silva" : "Renan Barber"}<small>${isClient ? "Cliente" : "Administrador"}</small></span>
                <a href="/src/frontend/pages/login.html" aria-label="Sair" data-logout>↗</a>
            </div>
        </aside>`;
});

document.querySelectorAll("[data-topbar]").forEach((slot) => {
    slot.innerHTML = `
        <header class="topbar">
            <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-controls="app-sidebar">☰</button>
            <div class="topbar-context"><span class="status-dot"></span>${document.body.dataset.area === "barber" ? "Operação online" : "Olá, Gabriel"}</div>
            <div class="topbar-actions"><button aria-label="Pesquisar">⌕</button><button aria-label="Notificações">♢<span class="notification-dot"></span></button></div>
        </header>`;
});

document.querySelector(".menu-toggle")?.addEventListener("click", () => {
    document.querySelector(".app-sidebar")?.classList.toggle("is-open");
});

document.querySelector("[data-logout]")?.addEventListener("click", () => {
    sessionStorage.removeItem("renanbarber_session");
});

document.querySelectorAll("[data-tabs]").forEach((tabGroup) => {
    tabGroup.addEventListener("click", (event) => {
        const tab = event.target.closest("button[data-target]");
        if (!tab) return;
        const scope = tabGroup.closest("[data-tab-scope]") || document;
        tabGroup.querySelectorAll("button").forEach((item) => item.classList.toggle("is-active", item === tab));
        scope.querySelectorAll("[data-tab-panel]").forEach((panel) => panel.hidden = panel.id !== tab.dataset.target);
    });
});

document.querySelectorAll("[data-selectable]").forEach((group) => {
    group.addEventListener("click", (event) => {
        const option = event.target.closest("button:not(:disabled)");
        if (!option) return;
        group.querySelectorAll("button").forEach((item) => item.classList.toggle("is-selected", item === option));
    });
});

document.querySelectorAll("[data-switch]").forEach((control) => {
    control.addEventListener("click", () => {
        control.classList.toggle("is-on");
        control.setAttribute("aria-pressed", String(control.classList.contains("is-on")));
    });
});
