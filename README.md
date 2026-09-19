# DISMAT Mini Magazzino

Applicazione web didattica per la gestione di un piccolo magazzino interno, sviluppata con Python, Flask e MySQL.

Il sistema gestisce articoli, giacenze, movimenti, fornitori, fotografie, autenticazione e un assistente interno denominato Martin.

## Funzionalita principali

- registrazione utenti;
- login e logout;
- protezione delle pagine tramite sessione Flask;
- dashboard con dati reali;
- gestione articoli;
- archivio e riattivazione degli articoli;
- gestione della scorta minima;
- registrazione di entrate e uscite;
- aggiornamento automatico della giacenza;
- storico dei movimenti;
- controllo della disponibilita prima di un'uscita;
- gestione fornitori;
- relazione molti-a-molti tra articoli e fornitori;
- caricamento e gestione fotografie;
- foto principale dell'articolo;
- tema chiaro e scuro;
- interfaccia responsive;
- assistente Martin con ricerca controllata sui dati del sistema.

## Architettura

Il progetto segue una struttura ispirata al modello MVC.

### Controller

`app.py`

Gestisce:

- route Flask;
- richieste GET e POST;
- form;
- sessioni;
- autenticazione;
- validazioni;
- redirect;
- endpoint JSON dell'assistente.

### Model

`models.py`

Contiene le funzioni Python che comunicano con MySQL e le query SQL relative a:

- articoli;
- categorie;
- utenti;
- fotografie;
- movimenti;
- fornitori;
- relazioni articolo-fornitore.

Le query utilizzano parametri `%s`.

`db.py`

Gestisce la connessione MySQL tramite `get_db()` e legge i parametri dal file `.env`.

### Logica assistente

`assistente.py`

Contiene la logica di Martin.

Martin utilizza una ricerca controllata sugli articoli e sui fornitori, con supporto a confronti approssimativi tramite `SequenceMatcher`.

Non genera query SQL libere e non inventa dati: le informazioni vengono recuperate tramite le funzioni presenti nel Model.

### View

`templates/`

Contiene i template HTML e Jinja2.

`static/`

Contiene CSS, JavaScript, immagini e file caricati.

## Struttura progetto

```text
dismat-magazzino/
|
|-- app.py
|-- models.py
|-- db.py
|-- assistente.py
|-- test_db.py
|
|-- database/
|   `-- schema.sql
|
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- articoli.html
|   |-- nuovo_articolo.html
|   |-- modifica_articolo.html
|   |-- dettaglio_articolo.html
|   |-- archivio_articoli.html
|   |-- movimenti.html
|   |-- fornitori.html
|   |-- nuovo_fornitore.html
|   |-- modifica_fornitore.html
|   |-- login.html
|   `-- register.html
|
|-- static/
|   |-- css/
|   |   `-- style.css
|   |-- js/
|   |   |-- theme.js
|   |   `-- assistente.js
|   |-- images/
|   |   |-- logo-dismat.jpeg
|   |   `-- martin.png
|   `-- uploads/
|       `-- .gitkeep
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md

## Diagrammi UML e modello ER

La documentazione di progetto comprende:

- Use Case Diagram;
- Activity Diagram;
- Sequence Diagram dei movimenti;
- Sequence Diagram dell'assistente Martin;
- schema dell'architettura MVC;
- diagramma ER del database;
- cardinalita delle relazioni.

I diagrammi completi sono disponibili in:

[docs/diagrammi.md](docs/diagrammi.md)


---

# Diagrammi UML e modello ER

## Use Case Diagram

```mermaid
flowchart LR
    U([Utente])

    U --> A[Registrazione e Login]
    U --> B[Visualizza Dashboard]
    U --> C[Gestisce Articoli]
    U --> D[Gestisce Fotografie]
    U --> E[Consulta Archivio]
    U --> F[Registra Movimenti]
    U --> G[Gestisce Fornitori]
    U --> H[Associa Fornitori agli Articoli]
    U --> I[Usa Assistente Martin]
    U --> J[Cambia Tema]
    U --> K[Logout]
```

## Activity Diagram - Registrazione di un movimento

```mermaid
flowchart TD
    A([Inizio]) --> B[Apri Movimenti]
    B --> C[Seleziona articolo]
    C --> D[Seleziona Entrata o Uscita]
    D --> E[Inserisce quantita]

    E --> F{Quantita valida?}

    F -- No --> G[Mostra errore]
    G --> E

    F -- Si --> H{Tipo movimento}

    H -- Entrata --> I[Aumenta giacenza]
    H -- Uscita --> J{Disponibilita sufficiente?}

    J -- No --> G
    J -- Si --> K[Diminuisce giacenza]

    I --> L[Registra movimento]
    K --> L

    L --> M[Commit database]
    M --> N[Mostra storico aggiornato]
    N --> O([Fine])
```

## Sequence Diagram - Movimento

```mermaid
sequenceDiagram
    actor U as Utente
    participant V as View
    participant C as app.py
    participant M as models.py
    participant DB as MySQL

    U->>V: Compila form movimento
    V->>C: POST /movimenti
    C->>C: Valida i dati
    C->>M: registra_movimento()

    alt ENTRATA
        M->>DB: UPDATE articolo + quantita
    else USCITA
        M->>DB: UPDATE articolo - quantita
    end

    M->>DB: INSERT movimento
    M->>DB: COMMIT

    DB-->>M: Operazione completata
    M-->>C: True
    C-->>V: Redirect
    V-->>U: Storico aggiornato
```

## Sequence Diagram - Assistente Martin

```mermaid
sequenceDiagram
    actor U as Utente
    participant JS as assistente.js
    participant C as app.py
    participant A as assistente.py
    participant M as models.py
    participant DB as MySQL

    U->>JS: Scrive una domanda
    JS->>C: POST /assistente
    C->>A: rispondi_assistente()
    A->>A: Interpreta la richiesta
    A->>M: Richiede dati
    M->>DB: Query parametrizzata
    DB-->>M: Risultato
    M-->>A: Dati
    A-->>C: Risposta controllata
    C-->>JS: JSON
    JS-->>U: Visualizza risposta
```

## Architettura MVC

```mermaid
flowchart LR
    U([Utente / Browser])

    V[View<br/>templates + static]
    C[Controller<br/>app.py]
    M[Model<br/>models.py]
    DB[(MySQL)]
    A[Assistente<br/>assistente.py]

    U --> V
    V --> C
    C --> M
    M --> DB

    C --> A
    A --> M

    DB --> M
    M --> C
    C --> V
    V --> U
```

## Diagramma ER

```mermaid
erDiagram

    CATEGORIA ||--o{ ARTICOLO : contiene
    ARTICOLO ||--o{ FOTO_ARTICOLO : possiede
    ARTICOLO ||--o{ MOVIMENTO : riguarda
    UTENTE ||--o{ MOVIMENTO : registra
    ARTICOLO ||--o{ ARTICOLO_FORNITORE : associa
    FORNITORE ||--o{ ARTICOLO_FORNITORE : associa

    CATEGORIA {
        int id PK
        varchar nome
        varchar descrizione
    }

    ARTICOLO {
        int id PK
        varchar codice
        varchar nome
        text descrizione
        decimal quantita
        decimal scorta_minima
        varchar unita_misura
        int categoria_id FK
        boolean attivo
    }

    FORNITORE {
        int id PK
        varchar ragione_sociale
        varchar referente
        varchar telefono
        varchar email
    }

    ARTICOLO_FORNITORE {
        int articolo_id PK, FK
        int fornitore_id PK, FK
    }

    FOTO_ARTICOLO {
        int id PK
        int articolo_id FK
        varchar nome_file
        varchar didascalia
        boolean principale
        boolean attiva
    }

    MOVIMENTO {
        int id PK
        int articolo_id FK
        int utente_id FK
        varchar tipo
        decimal quantita
        datetime data_movimento
        varchar note
    }

    UTENTE {
        int id PK
        varchar username
        varchar password_hash
        varchar nome
    }
```

## Cardinalita del database

```text
CATEGORIA  1 ----- N  ARTICOLO

ARTICOLO   1 ----- N  FOTO_ARTICOLO

ARTICOLO   1 ----- N  MOVIMENTO

UTENTE     1 ----- N  MOVIMENTO

ARTICOLO   N ----- M  FORNITORE
                  |
                  |
          ARTICOLO_FORNITORE
```

La relazione molti-a-molti tra `ARTICOLO` e `FORNITORE` viene risolta attraverso la tabella associativa `ARTICOLO_FORNITORE`.

