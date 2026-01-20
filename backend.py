import mysql.connector
import pandas as pd
import os
# --- Connexion MySQL ---

def get_connection():
    return mysql.connector.connect(
        host=os.environ["mysql.railway.internal"],
        user=os.environ["root"],
        password=os.environ["kKrMsXjWdgCvrFPjVddcQvcLQypURXlZ"],
        database=os.environ["railway"],
        port=int(os.environ["3306"])
    )

# --- Examens ---
def get_examens():
    conn = get_connection()
    query = """
        SELECT e.id, m.id AS module_id, m.nom AS module, p.id AS prof_id, p.nom AS professeur,
               l.nom AS salle, l.id AS salle_id, e.date_heure, e.duree_minutes, m.formation_id
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN professeurs p ON e.prof_id = p.id
        JOIN lieux_examen l ON e.salle_id = l.id
        ORDER BY e.date_heure
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- KPI ---
def get_kpi():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_global", conn)
    conn.close()
    if df.empty:
        return {}
    return df.iloc[0].to_dict()

# --- Conflits étudiants ---
def get_conflits_etudiants():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM conflits_etudiants", conn)
    conn.close()
    return df

# --- Formations (pour filtre département) ---
def get_formations():
    conn = get_connection()
    df = pd.read_sql("SELECT id, nom, dept_id FROM formations", conn)
    conn.close()
    return df

# --- Étudiants ---
def get_etudiants():
    conn = get_connection()
    df = pd.read_sql("SELECT id, nom, prenom, formation_id FROM etudiants", conn)
    conn.close()
    return df

def get_etudiants_ids():
    df = get_etudiants()
    return df["id"].tolist()

# --- Inscriptions (pour filtre étudiant) ---
def get_inscriptions():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM inscriptions", conn)
    conn.close()
    return df
