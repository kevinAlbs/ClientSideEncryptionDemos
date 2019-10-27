from flask import Flask, render_template, request, session, redirect, url_for, escape
import mongo

app = Flask(__name__)
app.secret_key = "example key"


@app.route("/")
def home():
    if "email" not in session:
        return redirect(url_for("login"))
    posts = mongo.get_posts(session["user_id"])
    return render_template(
        "home.html", posts=mongo.get_posts(session["user_id"]))


@app.route("/create_post", methods=["POST"])
def create_post():
    if "email" not in session:
        return redirect(url_for("login"))
    mongo.create_post(
        session["user_id"],
        request.form["title"],
        request.form["body"])
    return redirect(url_for("home"))


@app.route("/delete_all_data", methods=["GET"])
def delete_all_data():
    if "email" not in session:
        return redirect(url_for("login"))

    mongo.delete_all_data(session["user_id"])
    session.pop("email", None)
    session.pop("user_id", None)
    return render_template("delete_all_data.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    logged_in = False
    login_failed = False
    status_message = None

    if request.form["submit"] == "Login":
        # TODO verify with MongoDB.
        user_id, status_message = mongo.login(
            request.form["email"], request.form["pwd"])
        if user_id is not None:
            session["user_id"] = user_id
            session["email"] = request.form["email"]
            logged_in = True
    elif request.form["submit"] == "Register":
        # Insert in MongoDB.
        user_id, status_message = mongo.register(
            request.form["email"], request.form["pwd"])
        if user_id is not None:
            session["user_id"] = user_id
            session["email"] = request.form["email"]
            logged_in = True

    return render_template(
        "login.html",
        logged_in=logged_in,
        login_failed=login_failed,
        status_message=status_message)


@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("user_id", None)
    return render_template("logout.html")
