const assistantToggle = document.getElementById("assistantToggle");
const assistantPanel = document.getElementById("assistantPanel");
const assistantClose = document.getElementById("assistantClose");

const assistantForm = document.getElementById("assistantForm");
const assistantInput = document.getElementById("assistantInput");
const assistantMessages = document.getElementById("assistantMessages");

const assistantSuggestions = document.querySelectorAll(
    ".assistant-suggestion"
);


function apriAssistente() {
    assistantPanel.classList.add("open");
    assistantInput.focus();
}


function chiudiAssistente() {
    assistantPanel.classList.remove("open");
}


function aggiungiMessaggio(testo, tipo) {
    const messaggio = document.createElement("div");

    messaggio.classList.add(
        "assistant-message",
        tipo
    );

    messaggio.textContent = testo;

    assistantMessages.appendChild(messaggio);

    assistantMessages.scrollTop =
        assistantMessages.scrollHeight;
}


async function inviaMessaggio(testo) {

    if (!testo.trim()) {
        return;
    }

    aggiungiMessaggio(testo, "user");

    assistantInput.value = "";

    try {
        const response = await fetch("/assistente", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messaggio: testo
            })
        });

        const dati = await response.json();

        aggiungiMessaggio(
            dati.risposta,
            "bot"
        );

    } catch (errore) {
        aggiungiMessaggio(
            "Non riesco a contattare il sistema in questo momento.",
            "bot"
        );
    }
}


assistantToggle.addEventListener(
    "click",
    () => {
        if (assistantPanel.classList.contains("open")) {
            chiudiAssistente();
        } else {
            apriAssistente();
        }
    }
);


assistantClose.addEventListener(
    "click",
    chiudiAssistente
);


document.addEventListener(
    "keydown",
    event => {
        if (event.key === "Escape") {
            chiudiAssistente();
        }
    }
);


document.addEventListener(
    "click",
    event => {
        if (
            assistantPanel.classList.contains("open") &&
            !assistantPanel.contains(event.target) &&
            !assistantToggle.contains(event.target)
        ) {
            chiudiAssistente();
        }
    }
);


assistantForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();

        inviaMessaggio(
            assistantInput.value
        );
    }
);


assistantSuggestions.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            inviaMessaggio(
                button.dataset.message
            );
        }
    );
});

