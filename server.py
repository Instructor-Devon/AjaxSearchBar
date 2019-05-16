from flask import Flask, render_template, request, flash, redirect
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "adsf"

def validate(form_data):
    errors = []
    for field in form_data:
        if len(form_data[field]) < 1 and field != "confirm":
            errors.append(f"{field} is required")
    if field_exists(form_data["email"], "email"):
        errors.append("email is in use")
    if field_exists(form_data["username"], "username"):
        errors.append("username is in use")
    if form_data["password"] != form_data["confirm"]:
        errors.append("passwords do not match")
    return errors


def field_exists(username, field):
    mysql = connectToMySQL("flask")
    query = f"SELECT id FROM users WHERE {field} = %(username)s;"
    data = {
        "username": username
    }
    return len(mysql.query_db(query, data)) > 0

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def register():
    errors = validate(request.form)
    if errors:
        for e in errors:
            flash(e)
        return redirect("/")
    else:
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s,%(email)s, %(password)s)"
        data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        mysql = connectToMySQL("flask")
        mysql.query_db(query, data)
        return redirect("/")
        

@app.route("/search", methods=["POST"])
def search():
    if request.form["name"] == "":
        return ""
    mysql = connectToMySQL("flask")
    query = "SELECT username FROM users WHERE username LIKE %%(username)s;"
    data = {
        "username": request.form["name"] + "%"
    }
    users = mysql.query_db(query, data)
    return render_template("partials/users.html", users=users)

@app.route("/username", methods=["POST"])
def username():
    if request.form["username"] == "":
        return ""
    
    return render_template("partials/username.html", exists=field_exists(request.form["username"], "username"))
app.run(debug=True)
