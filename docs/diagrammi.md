# Diagrammi UML e modello ER

Questo documento raccoglie i principali diagrammi di analisi e progettazione del progetto DISMAT Mini Magazzino.

---

# 1. Use Case Diagram

```mermaid
flowchart LR
    U[Utente]

    U --> A[Registrazione e Login]
    U --> B[Visualizza Dashboard]
    U --> C[Gestisce Articoli]
    U --> D[Gestisce Foto]
    U --> E[Consulta Archivio]
    U --> F[Registra Movimenti]
    U --> G[Gestisce Fornitori]
    U --> H[Associa Fornitori agli Articoli]
    U --> I[Usa Assistente Martin]
    U --> J[Cambia Tema]
    U --> K[Logout]
```

---

# 2. Activity Diagram - Registrazione movimento

```mermaid
flowchart TD
    A[Utente apre Movimenti] --> B[Seleziona articolo]
    B --> C[Seleziona Entrata o Uscita]
    C --> D[Inserisce quantita]
    D --> E{Quantita maggiore di zero?}

    E -- No --> F[Mostra errore]
    E -- Si --> G{Tipo movimento}

    G -- Entrata --> H[Aumenta giacenza]
    G -- Uscita --> I{Giacenza sufficiente?}

    I -- No --> F
    I -- Si --> J[Diminuisce giacenza]

    H --> K[Inserisce record Movimento]
    J --> K

    K --> L[Commit database]
    L --> M[Storico aggiornato]
```

---

# 3. Sequence Diagram - Registrazione movimento

```mermaid
sequenceDiagram
    actor U as Utente
    participant V as View
    participant C as app.py
    participant M as models.py
    participant DB as MySQL

    U->>V: Compila form movimento
    V->>C: POST /movimenti
    C->>C: Valida quantita
    C->>M: registra_movimento()

    alt Entrata
        M->>DB: UPDATE articolo + quantita
    else Uscita
        M->>DB: UPDATE articolo - quantita se disponibile
    end

    M->>DB: INSERT movimento
    M->>DB: COMMIT
    DB-->>M: Operazione completata
    M-->>C: True
    C-->>V: Redirect /movimenti
    V-->>U: Mostra storico aggiornato
```

---

# 4. Sequence Diagram - Assistente Martin

```mermaid
sequenceDiagram
    actor U as Utente
    participant JS as assistente.js
    participant C as app.py
    participant A as assistente.py
    participant M as models.py
    participant DB as MySQL

    U->>JS: Scrive una domanda
    JS->>C: POST /assistente JSON
    C->>A: rispondi_assistente()
    A->>A: Normalizza e interpreta richiesta
    A->>M: Richiede dati controllati
    M->>DB: Query parametrizzata
    DB-->>M: Dati
    M-->>A: Risultati
    A-->>C: Risposta
    C-->>JS: JSON
    JS-->>U: Visualizza risposta di Martin
```

---

# 5. Diagramma MVC

```mermaid
flowchart LR
    U[Browser / Utente]

    U --> V[View<br/>templates + static]
    V --> C[Controller<br/>app.py]
    C --> M[Model<br/>models.py]
    M --> D[Database<br/>MySQL]

    C --> A[Assistente<br/>assistente.py]
    A --> M

    D --> M
    M --> C
    C --> V
    V --> U
```

---

# 6. Diagramma ER - Entity Relationship

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

    UTENTE {
        int id PK
        varchar username
        varchar password_hash
        varchar nome
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
```

---

# 7. Cardinalita principali

| Relazione | Cardinalita | Significato |
|---|---|---|
| Categoria - Articolo | 1:N | Una categoria puo contenere molti articoli |
| Articolo - Foto | 1:N | Un articolo puo avere piu fotografie |
| Articolo - Movimento | 1:N | Un articolo puo essere coinvolto in molti movimenti |
| Utente - Movimento | 1:N | Un utente puo registrare molti movimenti |
| Articolo - Fornitore | N:M | Un articolo puo avere piu fornitori e un fornitore puo fornire piu articoli |

La relazione N:M tra ARTICOLO e FORNITORE viene risolta tramite la tabella associativa ARTICOLO_FORNITORE.

---

# 8. Schema logico sintetico

```text
CATEGORIA
    1
    |
    N
ARTICOLO
    |
    +------ 1:N ------ FOTO_ARTICOLO
    |
    +------ 1:N ------ MOVIMENTO ------ N:1 ------ UTENTE
    |
    +------ 1:N ------ ARTICOLO_FORNITORE ------ N:1 ------ FORNITORE
```

---

## Nota progettuale

Il progetto utilizza una struttura modulare e prevalentemente procedurale.

I diagrammi UML rappresentano il comportamento e l'architettura dell'applicazione, mentre il diagramma ER descrive la struttura relazionale del database MySQL.
