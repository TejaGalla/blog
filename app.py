from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "replace-this-with-a-strong-secret-key"

DB_CONFIG = {
    "host": "localhost",
    "user": "teja",
    "password": "1234",
    "database": "flaskblog"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration (
            username VARCHAR(50) PRIMARY KEY,
            mobile VARCHAR(20) UNIQUE,
            email VARCHAR(100) UNIQUE,
            address VARCHAR(255),
            password VARCHAR(255)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT NOT NULL AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,
            slug VARCHAR(255) UNIQUE,
            poster_id VARCHAR(50),
            PRIMARY KEY (id),
            CONSTRAINT fk_poster_id
                FOREIGN KEY (poster_id) REFERENCES registration(username)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


init_db()


@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_posted DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("homepage.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        mobile = request.form["mobile"].strip()
        address = request.form["address"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        hashed_password = generate_password_hash(password)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO registration (username, mobile, email, address, password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (username, mobile, email, address, hashed_password)
            )
            conn.commit()
            flash("Registration successful. Please login.", "success")
            cursor.close()
            conn.close()
            return redirect(url_for("login"))

        except Error as e:
            flash(f"Registration failed: {e}", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registration WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))
    return render_template("admin.html")


@app.route("/addposts", methods=["GET", "POST"])
def addposts():
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        slug = request.form["slug"].strip()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO posts (title, content, slug, poster_id)
            VALUES (%s, %s, %s, %s)
            """,
            (title, content, slug, session["username"])
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Post added successfully.", "success")
        return redirect(url_for("viewpost"))

    return render_template("add_post.html")


@app.route("/viewpost")
def viewpost():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_posted DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("viewpost.html", posts=posts)


@app.route("/delete_post/<int:id>", methods=["POST"])
def delete_post(id):
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Post deleted successfully.", "info")
    return redirect(url_for("viewpost"))


@app.route("/updatepost/<int:id>", methods=["GET", "POST"])
def updatepost(id):
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        slug = request.form["slug"].strip()

        cursor.execute(
            """
            UPDATE posts
            SET title = %s, content = %s, slug = %s
            WHERE id = %s
            """,
            (title, content, slug, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Post updated successfully.", "success")
        return redirect(url_for("viewpost"))

    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("updatepost.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)