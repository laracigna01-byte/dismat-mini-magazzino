from db import get_db


def get_articoli():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT articolo.id,
               articolo.codice,
               articolo.nome,
               articolo.quantita,
               articolo.scorta_minima,
               articolo.unita_misura,
               categoria.nome AS categoria,
               foto_articolo.nome_file AS foto_principale
        FROM articolo
        INNER JOIN categoria
            ON articolo.categoria_id = categoria.id
        LEFT JOIN foto_articolo
            ON articolo.id = foto_articolo.articolo_id
            AND foto_articolo.principale = TRUE
            AND foto_articolo.attiva = TRUE
        WHERE articolo.attivo = TRUE
    """)

    articoli = cursor.fetchall()

    cursor.close()
    conn.close()

    return articoli


def get_articolo(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT articolo.*,
               categoria.nome AS categoria
        FROM articolo
        INNER JOIN categoria
            ON articolo.categoria_id = categoria.id
        WHERE articolo.id = %s
    """, (id,))

    articolo = cursor.fetchone()

    cursor.close()
    conn.close()

    return articolo


def get_categorie():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nome FROM categoria")
    categorie = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorie


def inserisci_articolo(dati):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO articolo
        (codice, nome, descrizione, quantita,
         scorta_minima, unita_misura, categoria_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, dati)

    conn.commit()

    cursor.close()
    conn.close()


def modifica_articolo(id, dati):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE articolo
        SET codice = %s,
            nome = %s,
            descrizione = %s,
            quantita = %s,
            scorta_minima = %s,
            unita_misura = %s,
            categoria_id = %s
        WHERE id = %s
    """, dati + (id,))

    conn.commit()

    cursor.close()
    conn.close()


def disattiva_articolo(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE articolo SET attivo = FALSE WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_articoli_disattivati():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT articolo.id,
               articolo.codice,
               articolo.nome,
               articolo.quantita,
               articolo.scorta_minima,
               articolo.unita_misura,
               categoria.nome AS categoria
        FROM articolo
        INNER JOIN categoria
            ON articolo.categoria_id = categoria.id
        WHERE articolo.attivo = FALSE
    """)

    articoli = cursor.fetchall()

    cursor.close()
    conn.close()

    return articoli


def riattiva_articolo(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE articolo SET attivo = TRUE WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()



def get_foto_articolo(articolo_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id,
               articolo_id,
               nome_file,
               didascalia,
               principale
        FROM foto_articolo
        WHERE articolo_id = %s
          AND attiva = TRUE
        ORDER BY principale DESC, id ASC
    """, (articolo_id,))

    foto = cursor.fetchall()

    cursor.close()
    conn.close()

    return foto


def inserisci_foto_articolo(articolo_id, nome_file, didascalia, principale):
    conn = get_db()
    cursor = conn.cursor()

    if principale:
        cursor.execute(
            "UPDATE foto_articolo SET principale = FALSE WHERE articolo_id = %s",
            (articolo_id,)
        )

    cursor.execute("""
        INSERT INTO foto_articolo
        (articolo_id, nome_file, didascalia, principale)
        VALUES (%s, %s, %s, %s)
    """, (
        articolo_id,
        nome_file,
        didascalia,
        principale
    ))

    conn.commit()

    cursor.close()
    conn.close()




def disattiva_foto_articolo(foto_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE foto_articolo
        SET attiva = FALSE,
            principale = FALSE
        WHERE id = %s
    """, (foto_id,))

    conn.commit()

    cursor.close()
    conn.close()


def get_utente_by_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id,
               username,
               password_hash,
               nome
        FROM utente
        WHERE username = %s
    """, (username,))

    utente = cursor.fetchone()

    cursor.close()
    conn.close()

    return utente


def inserisci_utente(nome, username, password_hash):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO utente
        (nome, username, password_hash)
        VALUES (%s, %s, %s)
    """, (
        nome,
        username,
        password_hash
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_movimenti():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT movimento.*,
               articolo.codice AS codice_articolo,
               articolo.nome AS articolo,
               utente.nome AS utente
        FROM movimento
        INNER JOIN articolo
            ON movimento.articolo_id = articolo.id
        INNER JOIN utente
            ON movimento.utente_id = utente.id
        ORDER BY movimento.data_movimento DESC
    """)

    movimenti = cursor.fetchall()

    cursor.close()
    conn.close()

    return movimenti


def registra_movimento(articolo_id, utente_id, tipo, quantita, note):
    conn = get_db()
    cursor = conn.cursor()

    if tipo == "ENTRATA":
        cursor.execute("""
            UPDATE articolo
            SET quantita = quantita + %s
            WHERE id = %s
              AND attivo = TRUE
        """, (quantita, articolo_id))

    elif tipo == "USCITA":
        cursor.execute("""
            UPDATE articolo
            SET quantita = quantita - %s
            WHERE id = %s
              AND attivo = TRUE
              AND quantita >= %s
        """, (quantita, articolo_id, quantita))

    else:
        cursor.close()
        conn.close()
        return False

    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO movimento
        (articolo_id, utente_id, tipo, quantita, note)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        articolo_id,
        utente_id,
        tipo,
        quantita,
        note
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return True

