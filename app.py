from flask import Flask
from flask import request
from flask import render_template
from logic import generate


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def display():
    if request.method == "GET":
        return render_template("input_form.html")
    else:
        id_type = request.form["ID"]
        id_ = int(request.form["id_value"])
        html_content = generate(id_type, id_)
        return html_content


if __name__ == "__main__":
    app.debug = True
    app.run()
