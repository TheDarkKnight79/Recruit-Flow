import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Grundkonfiguration der Seite
st.set_page_config(
    page_title="Recruit Flow Pro",
    page_icon="🚀",
    layout="wide"
)

# 2. Header & Logo
col1, col2 = st.columns([1, 5])
with col1:
    # Falls du kein logo.png hast, wird dieser Teil einfach übersprungen
    try:
        st.image("logo.png", width=100)
    except:
        st.write("🚀") 

with col2:
    st.title("Recruit Flow - Dashboard")
    st.markdown("*Status-Tracking & Bewerber-Übersicht*")

# 3. Beispieldaten (Diese würdest du später durch deine Excel/Datenbank ersetzen)
data = {
    "Name": ["Max Müller", "Anna Schmidt", "Erika Mustermann", "John Doe", "Sabine Sonnenschein", 
             "Lukas Läufer", "Julia Jäger", "Markus Meister", "Sven Schreiber", "Petra Pan"],
    "Status": ["Kontaktiert", "Eingeladen", "Kontaktiert", "Abgelehnt", "Kontaktiert", 
               "Kontaktiert", "Eingeladen", "Kontaktiert", "Kontaktiert", "Kontaktiert"],
    "Datum": ["2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05",
              "2024-05-06", "2024-05-07", "2024-05-08", "2024-05-09", "2024-05-10"],
    "Position": ["IT-Support", "HR Manager", "Software Entwickler", "Sales", "IT-Support",
                 "Marketing", "Software Entwickler", "IT-Support", "Sales", "HR Manager"]
}
df = pd.DataFrame(data)

# --- Diesen Teil in deinem Code suchen und anpassen ---

# 4. Sidebar für Filter (Damit sie links permanent erscheint)
with st.sidebar:
    st.header("Filter & Optionen")
    st.markdown("Nutze diese Filter, um die Ansicht anzupassen.")
    
    # Beispiel für einen interaktiven Filter in der Sidebar
    status_filter = st.multiselect(
        "Status auswählen:",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )
    
    st.divider()
    st.info("Präsentations-Modus: Aktiv")

# 5. Daten basierend auf Sidebar-Filter filtern
df_filtered = df[df["Status"].isin(status_filter)]

# 6. Kennzahlen (KPIs) - jetzt mit gefilterten Daten
st.subheader("Quick Stats")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Bewerber (gefiltert)", len(df_filtered))
kpi2.metric("Status: Kontaktiert", len(df_filtered[df_filtered["Status"] == "Kontaktiert"]))
kpi3.metric("Status: Eingeladen", len(df_filtered[df_filtered["Status"] == "Eingeladen"]))

# ... (Rest des Codes wie gehabt, aber df durch df_filtered ersetzen)
# 6. Footer
st.divider()
st.caption("Recruit Flow Pro V1.0 | Bereit für die Präsentation morgen")