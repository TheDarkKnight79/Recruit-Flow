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

# 4. Kennzahlen (KPIs) oben anzeigen
st.subheader("Quick Stats")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Bewerber Gesamt", len(df))
kpi2.metric("Status: Kontaktiert", len(df[df["Status"] == "Kontaktiert"]))
kpi3.metric("Status: Eingeladen", len(df[df["Status"] == "Eingeladen"]))

st.divider()

# 5. Hauptbereich: Grafik & Liste
left_column, right_column = st.columns([1, 1])

with left_column:
    st.subheader("Status-Verteilung")
    fig = px.pie(df, names='Status', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with right_column:
    st.subheader("Bewerber: Status 'Kontaktiert'")
    
    # Filter für die Liste
    df_kontaktiert = df[df["Status"] == "Kontaktiert"]
    
    # LÖSUNG FÜR DEIN PROBLEM: st.dataframe mit fester Höhe und Scrollbalken
    # 'use_container_width' sorgt dafür, dass es die Spalte ausfüllt
    # 'height=300' erzwingt den Scrollbalken, wenn die Liste länger wird
    st.dataframe(
        df_kontaktiert, 
        use_container_width=True, 
        height=300, 
        hide_index=True
    )
    
    st.info("💡 Du kannst in der Tabelle oben rechts auf das Vergrößern-Icon klicken oder Spalten sortieren.")

# 6. Footer
st.divider()
st.caption("Recruit Flow Pro V1.0 | Bereit für die Präsentation morgen")