const tabs = document.querySelectorAll(".auth-tab");
const forms = document.querySelectorAll(".auth-form");

function activateForm(tab) {
    tabs.forEach((item) => item.classList.toggle("is-active", item === tab));
    forms.forEach((form) => {
        const active = form.id === tab.dataset.form;
        form.classList.toggle("is-active", active);
        form.hidden = !active;
    });
}

tabs.forEach((tab) => tab.addEventListener("click", () => activateForm(tab)));
document.querySelectorAll("[data-password-toggle]").forEach((button) => button.addEventListener("click", () => {
    const input = document.getElementById(button.dataset.passwordToggle);
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    button.textContent = show ? "Ocultar" : "Mostrar";
}));
