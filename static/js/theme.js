const body = document.body;
const buttons = document.querySelectorAll(".theme-btn");

function setTheme(theme) {
    body.classList.remove("dark-theme", "light-theme");
    body.classList.add(theme + "-theme");

    buttons.forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.theme === theme
        );
    });

    localStorage.setItem("theme", theme);
}

const savedTheme = localStorage.getItem("theme") || "dark";

setTheme(savedTheme);

buttons.forEach(button => {
    button.addEventListener("click", () => {
        setTheme(button.dataset.theme);
    });
});
