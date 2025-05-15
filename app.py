from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    sha224 = None
    sha256 = None
    hash_type = "both"

    if request.method == "POST":
        text = request.form["text"]
        hash_type = request.form["hash_type"]

        if hash_type == "sha224" or hash_type == "both":
            sha224 = hashlib.sha224(text.encode()).hexdigest()

        if hash_type == "sha256" or hash_type == "both":
            sha256 = hashlib.sha256(text.encode()).hexdigest()

    return render_template("index.html", text=text, sha224=sha224, sha256=sha256, hash_type=hash_type)

if __name__ == "__main__":
    app.run(debug=True)
