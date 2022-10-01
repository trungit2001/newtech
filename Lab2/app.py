from flask import Flask, redirect, url_for, render_template, request, abort

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello")
def hello_world():
    return "Hello, World!"


@app.route("/hello/<name>")
def hello_name(name):
    return "Hello, %s!" % name


@app.route("/blog/<int:postID>")
def show_blog(postID: int):
    return "Blog number %d" % postID


@app.route("/rev/<float:revNo>")
def revision(revNo: float):
    return "Revision number %f" % revNo


@app.route("/admin")
def hello_admin():
    return "Hello, Admin!"


@app.route("/guest/<guest>")
def hello_guest(guest: str):
    return "Hello %s as Guest" % guest


@app.route("/user/<name>")
def hello_user(name: str):
    if name == "admin":
        return redirect(url_for("hello_admin"))
    else:
        return redirect(url_for("hello_guest", guest=name))


@app.route("/success/<username>/<password>")
def success(username: str, password: str):
    return render_template("welcome.html", name=username)


@app.route("/signin")
def sign_in():
    return render_template("login.html")


@app.errorhandler(404)
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return redirect(url_for('success', username=username, password=password))
    else:
        return render_template("page_not_found.html"), 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )
