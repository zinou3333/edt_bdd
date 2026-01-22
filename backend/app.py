from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_HOST = "sql7.freesqldatabase.com"
DB_USER = "sql7814784"
DB_PASSWORD = "taTn1hnK6N"
DB_NAME = "sql7814784"
DB_PORT = 3306

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

@app.route("/examens")
def examens():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, m.nom AS module, p.nom AS professeur,
               l.nom AS salle, e.date_heure, e.duree_minutes
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN professeurs p ON e.prof_id = p.id
        JOIN lieux_examen l ON e.salle_id = l.id
        ORDER BY e.date_heure
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/kpi")
def kpi():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kpi_global")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
