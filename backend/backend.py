from flask import Flask, jsonify
import mysql.connector
import pandas as pd
import os

app = Flask(__name__)

# ---------- Connexion MySQL ----------

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "sql7.freesqldatabase.com"),
        user=os.environ.get("MYSQLUSER", "sql7814784"),
        password=os.environ.get("MYSQLPASSWORD", "taTn1hnK6N"),
        database=os.environ.get("MYSQLDATABASE", "sql7814784s"),
        port=int(os.environ.get("MYSQLPORT", 3306))
    )

# ---------- Routes API ----------

@app.route("/examens")
def examens():
    conn = get_connection()
    query = """
        SELECT e.id, m.id AS module_id, m.nom AS module,
               p.id AS prof_id, p.nom AS professeur,
               l.nom AS salle, l.id AS salle_id,
               e.date_heure, e.duree_minutes, m.formation_id
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN professeurs p ON e.prof_id = p.id
        JOIN lieux_examen l ON e.salle_id = l.id
        ORDER BY e.date_heure
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/kpi")
def kpi():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_global", conn)
    conn.close()
    return jsonify({} if df.empty else df.iloc[0].to_dict())

@app.route("/conflits")
def conflits():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM conflits_etudiants", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/formations")
def formations():
    conn = get_connection()
    df = pd.read_sql("SELECT id, nom, dept_id FROM formations", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/etudiants")
def etudiants():
    conn = get_connection()
    df = pd.read_sql("SELECT id, nom, prenom, formation_id FROM etudiants", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/")
def health():
    return {"status": "ok"}

# ---------- Run Flask ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)