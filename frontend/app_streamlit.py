import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "https://your-backend.onrender.com"  # replace with deployed backend URL

st.set_page_config(page_title="Optimisation EDT Examens", layout="wide")
st.title("Plateforme d’Optimisation des Emplois du Temps d’Examens")

# ================= FETCH DATA =================
@st.cache_data
def get_examens():
    try:
        response = requests.get(f"{BACKEND_URL}/examens")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur: {e}")
        return pd.DataFrame()

@st.cache_data
def get_kpi():
    try:
        response = requests.get(f"{BACKEND_URL}/kpi")
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        return {} if df.empty else df.iloc[0].to_dict()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur: {e}")
        return {}

# ================= DISPLAY =================
df_examens = get_examens()
if not df_examens.empty:
    st.subheader("Planning des examens")
    st.dataframe(df_examens, use_container_width=True)
else:
    st.warning("Aucune donnée disponible.")

kpi = get_kpi()
if kpi:
    cols = st.columns(3)
    cols[0].metric("Total Examens", kpi.get("total_examens", 0))
    cols[1].metric("Conflits Étudiants", kpi.get("conflits_etudiants", 0))
    cols[2].metric("Conflits Professeurs", kpi.get("conflits_professeurs", 0))
