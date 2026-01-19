# app.py
import streamlit as st
import backend

st.set_page_config(page_title="Optimisation EDT Examens", layout="wide")

st.title("🎓 Plateforme d’Optimisation des Emplois du Temps d’Examens")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "📅 Emplois du temps",
        "⚠️ Conflits",
        "📊 KPI Doyen",
        "⚙️ Génération EDT"
    ]
)

# ===============================
# EMPLOIS DU TEMPS
# ===============================
if menu == "📅 Emplois du temps":
    st.subheader("Emplois du temps des examens")
    df = backend.get_examens()
    st.dataframe(df, use_container_width=True)

# ===============================
# CONFLITS
# ===============================
elif menu == "⚠️ Conflits":
    tab1, tab2, tab3 = st.tabs(
        ["Étudiants", "Professeurs", "Salles"]
    )

    with tab1:
        st.write("Conflits étudiants (plus d’un examen par jour)")
        st.dataframe(backend.get_conflits_etudiants())

    with tab2:
        st.write("Conflits professeurs (>3 examens / jour)")
        st.dataframe(backend.get_conflits_professeurs())

    with tab3:
        st.write("Capacité des salles dépassée")
        st.dataframe(backend.get_conflits_salles())

# ===============================
# KPI DOYEN
# ===============================
elif menu == "📊 KPI Doyen":
    st.subheader("Indicateurs globaux")
    kpi = backend.get_kpi()
    st.metric("Total Examens", kpi["total_examens"][0])
    st.metric("Conflits Étudiants", kpi["conflits_etudiants"][0])
    st.metric("Conflits Professeurs", kpi["conflits_professeurs"][0])
    st.metric("Conflits Salles", kpi["conflits_salles"][0])

# ===============================
# GENERATION EDT
# ===============================
elif menu == "⚙️ Génération EDT":
    st.subheader("Génération automatique de l'EDT")

    if st.button("🚀 Lancer l’optimisation"):
        result = backend.generer_edt()
        st.success(result)
