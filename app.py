from flask import Flask, render_template, request, redirect, abort, url_for, session, flash
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "72ea4c21a9bf105d345ca826a833800fec2fd7ace47715a1c28427a6d3969633"

@app.route("/users")
def users():
    return ["renyu", "aoyu"]

@app.route("/user/<name>")
def user_name(name):
    return "Hello, {name}".format(name = escape(name))

@app.route("/user/<int:user_id>")
def user_id(user_id):
    return "<p>Hello, user id: {user_id}!</p>".format(user_id=user_id)

@app.route("/user/<path:user_path>")
def user_path(user_path):
    return "<p>Hello, user path: {user_path}!</p>".format(user_path=user_path)


@app.route("/project/")
def project():
    return "This is a project."

@app.route("/page")
def page():
    return "This is a page."

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)

@app.route("/upload", methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["the_file"]
        file.save("./files/{fn}".format(fn=secure_filename(file.filename)))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=the_file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/cookie", methods = ["GET", "POST"])
def cookies():
    cookies_dict = request.cookies
    username = request.cookies.get("username")
    return "Cookie: {cookies_str}, username: {username}".format(cookies_str = str(cookies_dict), username=username)

@app.route("/")
def index():
    # if "username" in session:
    #     return "Logged in as: {username}".format(username=session["username"])
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        app.logger.debug(request.form)
        session["username"] = request.form["username"]
        flash("redirecting to index")
        return redirect(url_for("index"))

    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route("/logout")
def logout():
    session.pop("username")
    flash("redirecting to index")
    return redirect(url_for("index"))


