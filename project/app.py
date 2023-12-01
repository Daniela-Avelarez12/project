import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///piercing.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
#@login_required
def index1():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("correo"):
            return ("must provide email")
        elif not request.form.get("password"):
            return ("must provide password")
        rows = db.execute("SELECT * FROM users WHERE correo = ?", request.form.get("correo"))
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password")
        session["user_id"] = rows[0]["user_id"]
        return redirect("/index")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        correo = request.form.get("correo")
        if not username:
            return ("ingrese un nombre de usuario válido.")
        if not password:
            return ("ingrese una contraseña")
        if not correo:
            return ("por favor, confirme su contraseña")
        id = db.execute("SELECT * FROM users WHERE username=?", username)
        if len(id) > 0:
            return ("el usuario ya existe")
        password = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash, correo) VALUES (?, ?, ?)", username, password, correo
        )
        return redirect("/login")


@app.route("/labret")
def labret():
    return render_template("labret.html")

@app.route("/banana")
#@login_required
def banana():
    return render_template("banana.html")

@app.route("/shopping")
#@login_required
def shopping():
    productos = db.execute("SELECT * FROM Producto")
    return render_template("shopping.html", productos=productos)

@app.route("/get_product/<int:id>",  methods=["GET", "POST"])
def get_product(id):
    productos = db.execute("SELECT * FROM Producto WHERE 	id = ?", id)
    print(productos)
    return render_template("carrito.html", productos=productos)

@app.route("/aros")
@login_required
def aros():
    return render_template("aros.html")

@app.route("/galeria")
#@login_required
def galeria():
    return render_template("galeria.html")

@app.route("/limpieza_de_perforaciones")
#@login_required
def limpieza_de_perforaciones():
    return render_template("limpieza_de_perforaciones.html")

@app.route("/limpieza_de_pieza")
#@login_required
def limpieza_de_pieza():
    return render_template("limpieza_de_pieza.html")

@app.route("/piercing_falsos")
#@login_required
def piercing_falsos():
    return render_template("piercing_falsos.html")

@app.route("/perforaciones")
#@login_required
def perforaciones():
    return render_template("perforaciones.html")

@app.route("/servicios")
#@login_required
def servicios():
    return render_template("servicios.html")

@app.route("/multicentro")
#@login_required
def multicentro():
    return render_template("multicentro.html")

@app.route("/altamira")
#@login_required
def altamira():
    return render_template("altamira.html")

@app.route("/pago", methods=["GET", "POST"])
def pago():
    return render_template("pago.html")

    #https://codepen.io/justinklemm/embed/kyMjjv/?theme-id=modal#result-box