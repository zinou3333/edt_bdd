from flask import Flask, render_template
import backend

app = Flask(__name__)

@app.route("/")
def index():
    examens = backend.get_examens()
    kpi = backend.get_kpi()
    conflits = backend.get_conflits_etudiants()
    return render_template(
        "index.html",
        examens=examens,
        kpi=kpi,
        conflits=conflits
    )

if __name__ == "__main__":
    app.run(debug=True)
