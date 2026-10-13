from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-demo-secret-key"

MAX_ATTEMPTS = 3


# Connect to the new XAMPP database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cyber_login_system"
    )


# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    attempts = session.get("attempts", 0)
    message = None

    if request.method == "POST":

        if attempts >= MAX_ATTEMPTS:
            return render_template(
                "login.html",
                message="Account temporarily blocked!"
            )

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()

            if user and check_password_hash(
                user["password_hash"], password
            ):
                session.clear()
                session["logged_in"] = True
                session["username"] = user["username"]

                cursor.execute(
                    """
                    INSERT INTO login_logs
                    (username, status, ip_address)
                    VALUES (%s, %s, %s)
                    """,
                    (username, "SUCCESS", request.remote_addr)
                )
                db.commit()

                return redirect(url_for("welcome"))

            attempts += 1
            session["attempts"] = attempts

            cursor.execute(
                """
                INSERT INTO login_logs
                (username, status, ip_address)
                VALUES (%s, %s, %s)
                """,
                (username or "unknown", "FAILED", request.remote_addr)
            )
            db.commit()

            if attempts >= MAX_ATTEMPTS:
                message = "Account temporarily blocked!"
            else:
                message = (
                    "Invalid username or password! "
                    f"Attempts remaining: {MAX_ATTEMPTS - attempts}"
                )

        finally:
            cursor.close()
            db.close()

    return render_template("login.html", message=message)


# Welcome dashboard
@app.route("/welcome")
def welcome():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "welcome.html",
        username=session.get("username", "Admin")
    )


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Reset the demo login-attempt counter
@app.route("/reset")
def reset():
    session.pop("attempts", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)