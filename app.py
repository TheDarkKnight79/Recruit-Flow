import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Grundkonfiguration der Seite
st.set_page_config(
    page_title="Recruit Flow Pro",
    page_icon="🚀",
    layout="wide"
)

# --- SIDEBAR (Original-Zustand) ---
with st.sidebar:
    # Versucht das Logo zu laden, falls vorhanden
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.title("🚀 Recruit Flow")
    
    st.header("Navigation")
    st.info("📍 Dashboard-Übersicht")
    
    st.divider()
    st.caption("Version 1.0 | Status: Online")

# --- HAUPTBEREICH ---
st.title("Recruit Flow - Dashboard")
st.markdown("*Status-Tracking & Bewerber-Management*")

# 2. Datenquelle (Beispieldaten - hier kannst du später deine Excel einlesen)
data = {
    "Name": ["Max Müller", "Anna Schmidt", "Erika Mustermann", "John Doe", "Sabine Sonnenschein", 
             "Lukas Läufer", "Julia Jäger", "Markus Meister", "Sven Schreiber", "Petra Pan",
             "Christian Cloud", "Melanie Markt", "Thomas Test"],
    "Status": ["Kontaktiert", "Eingeladen", "Kontaktiert", "Abgelehnt", "Kontaktiert", 
               "Kontaktiert", "Eingeladen", "Kontaktiert", "Kontaktiert", "Kontaktiert",
               "Kontaktiert", "Eingeladen", "Kontaktiert"],
    "Datum": ["2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05",
              "2024-05-06", "2024-05-07", "2024-05-08", "2024-05-09", "2024-05-10",
              "2024-05-11", "2024-05-12", "2024-05-13"],
    "Position": ["IT-Support", "HR Manager", "Software Entwickler", "Sales", "IT-Support",
                 "Marketing", "Software Entwickler", "IT-Support", "Sales", "HR Manager",
                 "Azure Admin", "Marketing", "IT-Support"]
}
df = pd.DataFrame(data)

# 3. Kennzahlen (KPIs) in der oberen Reihe
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Bewerber Gesamt", len(df))
kpi2.metric("Status: Kontaktiert", len(df[df["Status"] == "Kontaktiert"]))
kpi3.metric("Status: Eingeladen", len(df[df["Status"] == "Eingeladen"]))

st.divider()

# 4. Layout: Grafik links, Scrollbare Liste rechts
col_grafik, col_liste = st.columns([1, 1])

with col_grafik:
    st.subheader("Status-Verteilung")
    fig = px.pie(
        df, 
        names='Status', 
        hole=0.4, 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    # Entfernt unnötige Ränder um die Grafik
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_liste:
    st.subheader("Bewerber: Status 'Kontaktiert'")
    
    # Filtert die Daten für die Anzeige
    df_kontaktiert = df[df["Status"] == "Kontaktiert"]
    
    # DIE SCROLLBARE TABELLE
    # height=350 erzwingt den Scrollbalken innerhalb der Box
    st.dataframe(
        df_kontaktiert, 
        use_container_width=True, 
        height=350, 
        hide_index=True
    )
    
    st.caption("💡 Nutze das Mausrad innerhalb der Tabelle zum Scrollen.")

# 5. Footer
st.divider()
st.caption("© 2024 Recruit Flow Pro | Internes Management Tool")