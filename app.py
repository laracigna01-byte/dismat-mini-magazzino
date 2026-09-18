import os
from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from models import (
    get_articoli,
    get_articolo,
    get_categorie,
    inserisci_articolo,
    modifica_articolo,
    disattiva_articolo,
    get_articoli_disattivati,
    riattiva_articolo,
    get_foto_articolo,
    inserisci_foto_articolo,
    disattiva_foto_articolo,
    get_utente_by_username,
    inserisci_utente,
    get_movimenti,
    registra_movimento
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.before_request
def richiedi_login():
    pagine_pubbliche = ["login", "registrazione", "static"]

    if request.endpoint not in pagine_pubbliche and "utente_id" not in session:
        return redirect(url_for("login"))


@app.route("/registrazione", methods=["GET", "POST"])
def registrazione():
    errore = None

    if request.method == "POST":
        nome = request.form["nome"]
        username = request.form["username"]
        password = request.form["password"]
        conferma_password = request.form["conferma_password"]

        if password != conferma_password:
            errore = "Le password non coincidono."

        elif get_utente_by_username(username):
            errore = "Username già utilizzato."

        else:
            password_hash = generate_password_hash(
                password,
                method="pbkdf2:sha256"
            )

            inserisci_utente(
                nome,
                username,
                password_hash
            )

            return redirect(url_for("login"))

    return render_template(
        "register.html",
        errore=errore
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    errore = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        utente = get_utente_by_username(username)

        if utente and check_password_hash(utente["password_hash"], password):
            session["utente_id"] = utente["id"]
            session["nome"] = utente["nome"]

            return redirect(url_for("home"))

        errore = "Username o password non corretti."

    return render_template("login.html", errore=errore)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/movimenti", methods=["GET", "POST"])
def movimenti():
    errore = None

    if request.method == "POST":
        articolo_id = request.form["articolo_id"]
        tipo = request.form["tipo"]
        quantita = float(request.form["quantita"])
        note = request.form.get("note", "")

        if quantita <= 0:
            errore = "La quantità deve essere maggiore di zero."

        else:
            registrato = registra_movimento(
                articolo_id,
                session["utente_id"],
                tipo,
                quantita,
                note
            )

            if registrato:
                return redirect(url_for("movimenti"))

            errore = "Movimento non registrato. Controlla la quantità disponibile."

    articoli = get_articoli()
    storico = get_movimenti()

    return render_template(
        "movimenti.html",
        articoli=articoli,
        movimenti=storico,
        errore=errore
    )


@app.route("/")
def home():
    articoli = get_articoli()
    return render_template("index.html", articoli=articoli)


@app.route("/articoli")
def articoli():
    articoli = get_articoli()
    return render_template("articoli.html", articoli=articoli)


@app.route("/articoli/nuovo", methods=["GET", "POST"])
def nuovo_articolo():

    if request.method == "POST":

        dati = (
            request.form["codice"],
            request.form["nome"],
            request.form["descrizione"],
            request.form["quantita"],
            request.form["scorta_minima"],
            request.form["unita_misura"],
            request.form["categoria_id"]
        )

        inserisci_articolo(dati)

        return redirect(url_for("home"))

    categorie = get_categorie()

    return render_template(
        "nuovo_articolo.html",
        categorie=categorie
    )


@app.route("/articoli/<int:id>")
def dettaglio_articolo(id):
    articolo = get_articolo(id)
    foto = get_foto_articolo(id)

    return render_template(
        "dettaglio_articolo.html",
        articolo=articolo,
        foto=foto
    )


@app.route("/articoli/<int:id>/foto", methods=["POST"])
def aggiungi_foto(id):

    file = request.files.get("foto")

    if not file or file.filename == "":
        return redirect(url_for("dettaglio_articolo", id=id))

    estensione = file.filename.rsplit(".", 1)[-1].lower()

    if estensione not in ["jpg", "jpeg", "png", "webp"]:
        return redirect(url_for("dettaglio_articolo", id=id))

    nome_originale = secure_filename(file.filename)
    nome_file = f"{uuid4().hex}_{nome_originale}"

    percorso = os.path.join(
        app.root_path,
        "static",
        "uploads",
        nome_file
    )

    file.save(percorso)

    didascalia = request.form.get("didascalia", "")
    principale = 1 if request.form.get("principale") else 0

    inserisci_foto_articolo,
    disattiva_foto_articolo(
        id,
        nome_file,
        didascalia,
        principale
    )

    return redirect(url_for("dettaglio_articolo", id=id))


@app.route("/articoli/<int:articolo_id>/foto/<int:foto_id>/elimina", methods=["POST"])
def elimina_foto(articolo_id, foto_id):
    disattiva_foto_articolo(foto_id)

    return redirect(
        url_for("dettaglio_articolo", id=articolo_id)
    )


@app.route("/articoli/modifica/<int:id>", methods=["GET", "POST"])
def modifica(id):

    if request.method == "POST":

        dati = (
            request.form["codice"],
            request.form["nome"],
            request.form["descrizione"],
            request.form["quantita"],
            request.form["scorta_minima"],
            request.form["unita_misura"],
            request.form["categoria_id"]
        )

        modifica_articolo(id, dati)

        return redirect(url_for("home"))

    articolo = get_articolo(id)
    categorie = get_categorie()

    return render_template(
        "modifica_articolo.html",
        articolo=articolo,
        categorie=categorie
    )


@app.route("/articoli/disattiva/<int:id>", methods=["POST"])
def disattiva(id):
    disattiva_articolo(id)
    return redirect(url_for("home"))


@app.route("/articoli/archivio")
def archivio_articoli():
    articoli = get_articoli_disattivati()

    return render_template(
        "archivio_articoli.html",
        articoli=articoli
    )


@app.route("/articoli/riattiva/<int:id>", methods=["POST"])
def riattiva(id):
    riattiva_articolo(id)
    return redirect(url_for("archivio_articoli"))


if __name__ == "__main__":
    app.run(debug=True)















