import os
import numpy as np

from flask import (
    Flask, flash, 
    redirect, url_for, 
    render_template, request, 
    abort
)
from models.model import FashionMNIST
from werkzeug.utils import secure_filename

from PIL import Image


UPLOAD_FOLDER = './static/imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
model = FashionMNIST(input_shape=(28, 28, 1))
model.load_weights('./models/weights/fashion_mnist.h5')


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def invalid_route(e):
    return render_template("page_not_found.html"), 404


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("upload.html")

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            abort(404)

        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for("predict", filename=filename))
        else:
            abort(404)
    else:
        abort(404)


@app.route("/predict/<string:filename>", methods=["GET", "POST"])
def predict(filename):
    file = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file):
        print('No such file', filename)
        abort(404)
    else:
        img = Image.open(file)
        img = np.expand_dims(img, -1)
        label, confidence = model.predict(img)
        
        if label and confidence:
            return render_template("prediction.html", img_src='../static/imgs/' + filename, label=label, confidence=confidence)
        else:
            abort(404)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )
