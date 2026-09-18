# DISMAT Mini Magazzino

Applicazione web didattica per la gestione di un piccolo magazzino, realizzata con Flask e MySQL.

## Struttura MVC

### CONTROLLER
app.py

Gestisce:
- route Flask
- richieste GET e POST
- form
- sessione
- login e logout
- redirect
- collegamento tra Model e View

### MODEL
models.py

Contiene:
- funzioni Python per l'accesso ai dati
- query SQL
- gestione articoli
- gestione utenti
- gestione movimenti

db.py

Gestisce la connessione al database MySQL tramite get_db().

### VIEW
templates/

Contiene le pagine HTML e i template Jinja2.

static/

Contiene:
- CSS
- JavaScript
- immagini
- file caricati

## Schema

Browser
  |
  v
Controller - app.py
  |
  +--> Model - models.py
  |       |
  |       v
  |     MySQL
  |
  v
View - templates + static
  |
  v
Browser

## Tecnologie

- Python
- Flask
- MySQL
- Jinja2
- Bootstrap 5
- CSS
- JavaScript
- Werkzeug
- python-dotenv
- mysql-connector-python

## Principio del progetto

Il progetto è mantenuto volutamente semplice: poche funzioni, responsabilità chiare e codice facilmente leggibile e spiegabile.

## Albero del progetto

```text
dismat-magazzino/
|
|-- app.py                  CONTROLLER
|-- models.py               MODEL
|-- db.py                   Supporto database
|
|-- templates/              VIEW
|   |-- base.html
|   |-- index.html
|   |-- articoli.html
|   |-- nuovo_articolo.html
|   |-- modifica_articolo.html
|   |-- dettaglio_articolo.html
|   |-- archivio_articoli.html
|   |-- movimenti.html
|   |-- login.html
|   `-- register.html
|
|-- static/                 VIEW
|   |-- css/
|   |-- js/
|   |-- images/
|   `-- uploads/
|
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Diagrammi UML

### Use Case

```mermaid
flowchart LR
    U[Utente]

    U --> A[Registrazione e Login]
    U --> B[Visualizza Dashboard]
    U --> C[Gestisce Articoli]
    U --> D[Gestisce Foto]
    U --> E[Consulta Archivio]
    U --> F[Registra Movimenti]
    U --> G[Logout]
```

### Activity Diagram - Registrazione di un movimento

```mermaid
flowchart TD
    A[Utente apre Movimenti] --> B[Seleziona articolo]
    B --> C[Seleziona Entrata o Uscita]
    C --> D[Inserisce quantita]
    D --> E{Quantita valida?}

    E -- No --> F[Mostra errore]
    E -- Si --> G{Tipo movimento}

    G -- Entrata --> H[Aumenta giacenza]
    G -- Uscita --> I{Giacenza sufficiente?}

    I -- No --> F
    I -- Si --> J[Diminuisce giacenza]

    H --> K[Registra movimento]
    J --> K

    K --> L[Aggiorna storico]
```

### Sequence Diagram - Registrazione di un movimento

```mermaid
sequenceDiagram
    actor U as Utente
    participant V as View
    participant C as app.py
    participant M as models.py
    participant DB as MySQL

    U->>V: Compila il form
    V->>C: POST /movimenti
    C->>M: registra_movimento()
    M->>DB: UPDATE articolo
    M->>DB: INSERT movimento
    DB-->>M: Operazione completata
    M-->>C: True
    C-->>V: Redirect /movimenti
    V-->>U: Mostra storico aggiornato
```

### Modello delle entita

```mermaid
classDiagram

    class Utente {
        id
        username
        password_hash
        nome
    }

    class Categoria {
        id
        nome
        descrizione
    }

    class Articolo {
        id
        codice
        nome
        quantita
        scorta_minima
        unita_misura
        attivo
    }

    class Fornitore {
        id
        ragione_sociale
        referente
        telefono
        email
    }

    class ArticoloFornitore {
        articolo_id
        fornitore_id
    }

    class FotoArticolo {
        id
        nome_file
        didascalia
        principale
        attiva
    }

    class Movimento {
        id
        tipo
        quantita
        data_movimento
        note
    }

    Categoria "1" --> "0..*" Articolo
    Articolo "1" --> "0..*" ArticoloFornitore
    Fornitore "1" --> "0..*" ArticoloFornitore
    Articolo "1" --> "0..*" FotoArticolo
    Articolo "1" --> "0..*" Movimento
    Utente "1" --> "0..*" Movimento
```
