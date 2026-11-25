from dotenv import load_dotenv

load_dotenv()
import config
import sqlite3
import os

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database import init_db
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.secret_key = config.SECRET_KEY
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("RENDER") == "true",
)

csrf = CSRFProtect(app)

# Создаём базу данных при запуске сайта
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")

        if check_password_hash(config.ADMIN_PASSWORD_HASH, password):
            session.clear()
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        return render_template("login.html", error="Неверный пароль")

    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    connection = sqlite3.connect("blackwood.db")
    connection.row_factory = sqlite3.Row

    appointments = connection.execute(
        "SELECT * FROM appointments ORDER BY id DESC"
    ).fetchall()

    total_appointments = len(appointments)

    new_appointments = sum(
        1 for appointment in appointments if appointment["status"] == "new"
    )

    completed_appointments = sum(
        1 for appointment in appointments if appointment["status"] == "completed"
    )

    connection.close()

    return render_template(
        "admin.html",
        appointments=appointments,
        total_appointments=total_appointments,
        new_appointments=new_appointments,
        completed_appointments=completed_appointments,
    )


@app.route("/admin/complete/<int:appointment_id>", methods=["POST"])
def complete_appointment(appointment_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    connection = sqlite3.connect("blackwood.db")

    connection.execute(
        "UPDATE appointments SET status = 'completed' WHERE id = ?", (appointment_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:appointment_id>", methods=["POST"])
def delete_appointment(appointment_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    connection = sqlite3.connect("blackwood.db")

    connection.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=False)
