
import os
import secrets
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask, flash, redirect, render_template,
    request, session, url_for
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(os.getenv("VERCEL"))


def exigir_login(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if not session.get("participante"):
            return redirect(url_for("entrar"))
        return funcao(*args, **kwargs)
    return verificar


@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    if request.method == "POST":
        senha = request.form.get("senha", "")

        if secrets.compare_digest(
            senha, os.environ["DEMO_PASSWORD"]
        ):
            session.clear()
            session["participante"] = True
            return redirect(url_for("inicio"))

        flash("Senha incorreta. Tente novamente.")

    return render_template(
        "index.html",
        autenticado=False
    )


@app.route("/")
@exigir_login
def inicio():
    return render_template(
        "index.html",
        autenticado=True
    )


@app.route("/sair", methods=["POST"])
@exigir_login
def sair():
    session.clear()
    return redirect(url_for("entrar"))


if __name__ == "__main__":
    app.run(debug=True)
