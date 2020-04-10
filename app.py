from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html", error=False, error_message="")


@app.route('/login', methods=["POST"])
def login_request():
    uname = request.form["uname"]
    passw = request.form["passw"]

    login = user.query.filter_by(username=uname, password=passw).first()
    if login is not None:
        return redirect("done")
    return render_template("login.html", error=True, error_message="Invalid credentials")


@app.route('/done', methods=["GET"])
def done():
    return render_template("done.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        passw = request.form['passw']

        register = user(username=uname, password=passw)
        db.session.add(register)
        db.session.commit()

        return redirect("login")
    return render_template("register.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
