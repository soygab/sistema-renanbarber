const tabs = document.querySelectorAll(".auth-tab");
const forms = document.querySelectorAll(".auth-form");

function activateForm(tab) {
    const targetId = tab.dataset.form;

    tabs.forEach((item) => {
        const isActive = item === tab;
        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-selected", String(isActive));
        item.tabIndex = isActive ? 0 : -1;
    });

    forms.forEach((form) => {
        const isActive = form.id === targetId;
        form.classList.toggle("is-active", isActive);
        form.hidden = !isActive;
    });
}

tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateForm(tab));
    tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;

        event.preventDefault();
        const step = event.key === "ArrowRight" ? 1 : -1;
        const nextTab = tabs[(index + step + tabs.length) % tabs.length];
        activateForm(nextTab);
        nextTab.focus();
    });
});

document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
        const input = document.getElementById(button.dataset.passwordToggle);
        const willShow = input.type === "password";

        input.type = willShow ? "text" : "password";
        button.textContent = willShow ? "Ocultar" : "Mostrar";
        button.setAttribute("aria-label", willShow ? "Ocultar senha" : "Mostrar senha");
        button.setAttribute("aria-pressed", String(willShow));
    });
});

const authFeedback = document.querySelector(".auth-feedback");

function completeAuthentication(role, email) {
    const destination = role === "barber"
        ? "/src/frontend/pages/barbeiro-home.html"
        : "/src/frontend/pages/cliente-home.html";

    sessionStorage.setItem("renanbarber_session", JSON.stringify({ role, email }));

    if (authFeedback) {
        authFeedback.hidden = false;
        authFeedback.textContent = role === "barber"
            ? "Acesso verificado. Abrindo o painel da equipe…"
            : "Acesso verificado. Abrindo sua área…";
    }

    window.setTimeout(() => window.location.assign(destination), 350);
}

document.querySelector("#login-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) return;

    const email = String(new FormData(form).get("email")).trim().toLowerCase();
    // Regra temporária do protótipo visual; o backend substituirá esta lista.
    const barberEmails = new Set([
        "barbeiro@renanbarber.com",
        "admin@renanbarber.com",
        "renan@renanbarber.com",
    ]);
    const role = barberEmails.has(email)
        ? "barber"
        : "client";

    completeAuthentication(role, email);
});

document.querySelector("#register-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) return;

    const email = String(new FormData(form).get("email")).trim().toLowerCase();
    completeAuthentication("client", email);
});
