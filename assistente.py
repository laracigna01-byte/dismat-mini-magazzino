from difflib import SequenceMatcher

from models import (
    get_articoli,
    get_fornitori,
    get_fornitori_articolo,
    get_movimenti
)


def normalizza(testo):
    return testo.lower().strip()


def somiglianza(testo, candidato):
    testo = normalizza(testo)
    candidato = normalizza(candidato)

    if candidato in testo:
        return 1.0

    punteggi = [SequenceMatcher(None, testo, candidato).ratio()]

    for parola in testo.split():
        punteggi.append(
            SequenceMatcher(None, parola, candidato).ratio()
        )

    return max(punteggi)


def trova_articolo(testo):
    articoli = get_articoli()
    testo_norm = normalizza(testo)

    parole_testo = set(
        testo_norm.replace("-", " ").split()
    )

    parole_da_ignorare = {
        "il", "lo", "la", "i", "gli", "le",
        "di", "del", "della", "dei", "delle",
        "in", "con", "per", "un", "una"
    }

    migliore = None
    punteggio_migliore = 0

    for articolo in articoli:
        codice = normalizza(str(articolo["codice"]))
        nome = normalizza(articolo["nome"])

        parole_nome = set(
            nome.replace("-", " ").split()
        ) - parole_da_ignorare

        if codice in testo_norm:
            return articolo

        if parole_testo.intersection(parole_nome):
            return articolo

        candidati = [
            articolo["codice"],
            articolo["nome"]
        ]

        punteggio = max(
            somiglianza(testo, candidato)
            for candidato in candidati
        )

        if punteggio > punteggio_migliore:
            migliore = articolo
            punteggio_migliore = punteggio

    if punteggio_migliore >= 0.55:
        return migliore

    return None


def trova_fornitore(testo):
    fornitori = get_fornitori()

    migliore = None
    punteggio_migliore = 0

    for fornitore in fornitori:
        candidati = [
            fornitore["ragione_sociale"],
            fornitore["referente"] or ""
        ]

        punteggio = max(
            somiglianza(testo, candidato)
            for candidato in candidati
            if candidato
        )

        if punteggio > punteggio_migliore:
            migliore = fornitore
            punteggio_migliore = punteggio

    if punteggio_migliore >= 0.55:
        return migliore

    return None


def risposta_fornitore(fornitore):
    return (
        f'{fornitore["ragione_sociale"]}\n'
        f'Referente: {fornitore["referente"] or "-"}\n'
        f'Telefono: {fornitore["telefono"] or "-"}\n'
        f'Email: {fornitore["email"] or "-"}'
    )


def risposta_articolo(articolo):
    return (
        f'{articolo["codice"]} - {articolo["nome"]}\n'
        f'Quantità: {articolo["quantita"]} {articolo["unita_misura"]}\n'
        f'Scorta minima: {articolo["scorta_minima"]} {articolo["unita_misura"]}'
    )


def rispondi_assistente(messaggio):
    testo = normalizza(messaggio)

    if not testo:
        return "Scrivi una richiesta."

    if testo in ["ciao", "salve", "buongiorno", "buonasera"]:
        return (
            "Ciao, sono Martin. Posso aiutarti a cercare "
            "articoli, fornitori, recapiti, scorte e movimenti."
        )

    if "aiuto" in testo or "cosa puoi fare" in testo:
        return (
            "Posso cercare articoli e fornitori, mostrare telefoni "
            "ed email, controllare le scorte e consultare gli ultimi movimenti."
        )

    if "scort" in testo and (
        "bass" in testo or
        "minim" in testo
    ):
        articoli = [
            articolo
            for articolo in get_articoli()
            if articolo["quantita"] <= articolo["scorta_minima"]
        ]

        if not articoli:
            return "Al momento non risultano articoli con scorta bassa."

        righe = ["Articoli con scorta bassa:"]

        for articolo in articoli:
            righe.append(
                f'- {articolo["codice"]} - {articolo["nome"]}: '
                f'{articolo["quantita"]} {articolo["unita_misura"]}'
            )

        return "\n".join(righe)

    if "moviment" in testo:
        movimenti = get_movimenti()[:5]

        if not movimenti:
            return "Non risultano movimenti registrati."

        righe = ["Ultimi movimenti:"]

        for movimento in movimenti:
            righe.append(
                f'- {movimento["tipo"]}: '
                f'{movimento["codice_articolo"]} - '
                f'{movimento["articolo"]}, '
                f'{movimento["quantita"]}'
            )

        return "\n".join(righe)

    frasi_elenco_fornitori = [
        "quali sono i fornitori",
        "elenco fornitori",
        "mostra i fornitori",
        "tutti i fornitori",
        "fornitori registrati"
    ]

    if any(frase in testo for frase in frasi_elenco_fornitori):
        fornitori = get_fornitori()

        if not fornitori:
            return "Non risultano fornitori registrati."

        righe = ["Fornitori registrati:"]

        for fornitore in fornitori:
            righe.append(
                f'- {fornitore["ragione_sociale"]} - '
                f'{fornitore["telefono"] or "telefono non disponibile"}'
            )

        return "\n".join(righe)

    articolo = trova_articolo(testo)

    if articolo and (
        "fornit" in testo or
        "chi fornisce" in testo
    ):
        fornitori = get_fornitori_articolo(articolo["id"])

        if not fornitori:
            return (
                f'Non risultano fornitori associati a '
                f'{articolo["codice"]} - {articolo["nome"]}.'
            )

        righe = [
            f'Fornitori di {articolo["codice"]} - {articolo["nome"]}:'
        ]

        for fornitore in fornitori:
            righe.append(
                f'- {fornitore["ragione_sociale"]} '
                f'({fornitore["telefono"] or "telefono non disponibile"})'
            )

        return "\n".join(righe)

    fornitore = trova_fornitore(testo)

    if fornitore:
        return risposta_fornitore(fornitore)

    if articolo:
        return risposta_articolo(articolo)

    if "come" in testo and "uscita" in testo:
        return (
            "Apri Movimenti, seleziona l'articolo, scegli Uscita, "
            "inserisci la quantità e premi Registra movimento."
        )

    if "come" in testo and "articolo" in testo:
        return (
            "Apri Articoli e premi Nuovo articolo. "
            "Compila i dati richiesti e salva."
        )

    if "archivio" in testo:
        return (
            "La sezione Archivio contiene gli articoli disattivati. "
            "Da lì puoi anche riattivarli."
        )

    return (
        "Non ho trovato una risposta sicura. "
        "Prova a indicare il nome di un articolo, un fornitore "
        "oppure chiedimi informazioni su scorte o movimenti."
    )


