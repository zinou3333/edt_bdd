import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Optimisation EDT Examens",
    layout="wide"
)

# === URL du backend déployé ===
BACKEND_URL = "https://tonbackend.onrender.com"  # <-- Remplace par ton URL Render/Railway

st.title("Plateforme d’Optimisation des Emplois du Temps d’Examens")

# --- Étape 1 : Choix du rôle utilisateur ---
role = st.sidebar.selectbox(
    "Sélectionnez votre rôle",
    [
        "Vice-doyen / Doyen",
        "Administrateur examens",
        "Chef de département",
        "Étudiant / Professeur"
    ]
)

# --- Étape 1b : Mot de passe pour certains rôles ---
password_ok = True

if role == "Vice-doyen / Doyen":
    pwd = st.sidebar.text_input("Mot de passe", type="password")
    if pwd != "0123":
        st.sidebar.warning("Mot de passe incorrect !")
        password_ok = False
elif role == "Administrateur examens":
    pwd = st.sidebar.text_input("Mot de passe", type="password")
    if pwd != "abcd":
        st.sidebar.warning("Mot de passe incorrect !")
        password_ok = False
elif role == "Chef de département":
    pwd = st.sidebar.text_input("Mot de passe", type="password")
    if pwd != "5678":
        st.sidebar.warning("Mot de passe incorrect !")
        password_ok = False

# --- Fonctions pour récupérer les données depuis le backend ---
@st.cache_data
def get_examens():
    return pd.DataFrame(requests.get(f"{BACKEND_URL}/examens").json())

@st.cache_data
def get_kpi():
    return requests.get(f"{BACKEND_URL}/kpi").json()

@st.cache_data
def get_conflits_etudiants():
    return pd.DataFrame(requests.get(f"{BACKEND_URL}/conflits").json())

@st.cache_data
def get_formations():
    return pd.DataFrame(requests.get(f"{BACKEND_URL}/formations").json())

@st.cache_data
def get_etudiants():
    return pd.DataFrame(requests.get(f"{BACKEND_URL}/etudiants").json())

# Pour l’exemple, on met un tableau vide pour inscriptions
def get_inscriptions():
    return pd.DataFrame(columns=["etudiant_id", "module_id"])

def get_etudiants_ids():
    return get_etudiants()["id"].tolist()

# --- Si mot de passe correct ou rôle sans mot de passe ---
if password_ok:
    if role == "Chef de département":
        dept_id = st.sidebar.number_input("ID du département", min_value=1, step=1)
    elif role == "Étudiant / Professeur":
        user_id = st.sidebar.number_input("Votre ID", min_value=1, step=1)

    if role == "Vice-doyen / Doyen":
        menu_options = ["Vue globale", "KPI Globaux"]
    elif role == "Administrateur examens":
        menu_options = ["Emplois du temps", "Détection conflits", "Optimisation EDT", "KPI Globaux"]
    elif role == "Chef de département":
        menu_options = ["Emplois du temps département", "Conflits par formation", "KPI Globaux"]
    else:
        menu_options = ["Mon planning"]

    menu = st.sidebar.selectbox("Menu", menu_options)

    def filter_examens_by_dept(df, dept_id):
        df = df.merge(get_formations(), left_on="formation_id", right_on="id")
        return df[df["dept_id"] == dept_id]

    def filter_examens_by_user(df, user_id):
        if user_id in get_etudiants_ids():
            inscriptions = get_inscriptions()
            exams_ids = inscriptions[inscriptions["etudiant_id"] == user_id]["module_id"].tolist()
            return df[df["module_id"].isin(exams_ids)]
        else:
            return df[df["prof_id"] == user_id]

    # --- Affichage ---
    if menu in ["Emplois du temps", "Emplois du temps département", "Mon planning", "Vue globale"]:
        st.subheader("Planning des examens")
        df_examens = get_examens()

        if menu == "Emplois du temps département":
            df_examens = filter_examens_by_dept(df_examens, dept_id)
        elif menu == "Mon planning":
            df_examens = filter_examens_by_user(df_examens, user_id)

        st.dataframe(df_examens, use_container_width=True)

    elif menu in ["Conflits Étudiants", "Détection conflits", "Conflits par formation"]:
        st.subheader("Détection des conflits")
        df_conflits = get_conflits_etudiants()

        if menu == "Conflits par formation":
            df_conflits = df_conflits.merge(get_etudiants(), left_on="etudiant_id", right_on="id")
            df_conflits = df_conflits[df_conflits["formation_id"] == dept_id]

        if df_conflits.empty:
            st.success("Aucun conflit détecté")
        else:
            st.error("Conflits détectés")
            st.dataframe(df_conflits, use_container_width=True)

    elif menu == "Optimisation EDT":
        st.subheader("Optimisation automatique des emplois du temps")
        st.info("Fonctionnalité à implémenter pour générer automatiquement les EDT et résoudre les conflits.")

    elif menu == "KPI Globaux":
        st.subheader("Indicateurs Globaux")
        kpi = get_kpi()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Examens", kpi.get("total_examens", 0))
        col2.metric("Conflits Étudiants", kpi.get("conflits_etudiants", 0))
        col3.metric("Conflits Professeurs", kpi.get("conflits_professeurs", 0))
        col4.metric("Conflits Salles", kpi.get("conflits_salles", 0))

else:
    st.error("Vous n’êtes pas autorisé à accéder à cette section. Mot de passe incorrect.")
