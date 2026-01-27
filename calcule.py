import streamlit as st

st.set_page_config(page_title="Moyenne Semestre", page_icon="📊")

st.title("📊 Calcul de la moyenne du semestre")

# Modules et coefficients
modules = {
    "AA": 3,
    "RA": 3,
    "BDDA": 3,
    "TAI": 3,
    "Cloud": 2,
    "APDS": 2,
    "Workshop": 1
}

st.write("### Saisir les notes (Examen / CC)")

total_points = 0
total_coeff = 0

for module, coeff in modules.items():
    st.subheader(f"{module} (Coeff {coeff})")

    examen = st.number_input(
        f"Note Examen - {module}",
        min_value=0.0,
        max_value=20.0,
        step=0.25,
        key=f"exam_{module}"
    )

    cc = st.number_input(
        f"Note CC - {module}",
        min_value=0.0,
        max_value=20.0,
        step=0.25,
        key=f"cc_{module}"
    )

    moyenne_module = 0.6 * examen + 0.4 * cc
    st.write(f"➡️ Moyenne du module : **{moyenne_module:.2f}**")

    total_points += moyenne_module * coeff
    total_coeff += coeff

if st.button("📌 Calculer la moyenne du semestre"):
    moyenne_semestre = total_points / total_coeff
    st.success(f"🎓 Moyenne générale du semestre : **{moyenne_semestre:.2f}**")
