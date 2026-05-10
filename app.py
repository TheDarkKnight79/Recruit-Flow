import streamlit as st
import pandas as pd
import datetime
import os
import json
import plotly.express as px
import random

# --- 1. SETUP & KONFIGURATION ---
st.set_page_config(page_title="Recruit-Flow CRM Pro", layout="wide", page_icon="🎯")

DB_FILE = "recruiting_db.csv"
SETTINGS_FILE = "budget_settings.json"
LOGO_FILE = "logo.png"

# Grobe Regionen-Koordinaten
GEO_REGIONS = {
    "0": {"name": "Ost (Leipzig/Dresden)", "lat": 51.2, "lon": 13.0},
    "1": {"name": "Nord-Ost (Berlin/Potsdam)", "lat": 52.5, "lon": 13.4},
    "2": {"name": "Nord (Hamburg/Kiel)", "lat": 53.8, "lon": 10.0},
    "3": {"name": "Mitte (Hannover/Kassel)", "lat": 52.0, "lon": 9.5},
    "4": {"name": "West (Dortmund/Düsseldorf)", "lat": 51.3, "lon": 7.0},
    "5": {"name": "Süd-West (Köln/Mainz)", "lat": 50.5, "lon": 7.5},
    "6": {"name": "Süd-West (Frankfurt/Saar)", "lat": 49.5, "lon": 8.5},
    "7": {"name": "Süd (Stuttgart/Karlsruhe)", "lat": 48.5, "lon": 9.0},
    "8": {"name": "Süd (München/Augsburg)", "lat": 48.2, "lon": 11.5},
    "9": {"name": "Süd-Ost (Nürnberg/Erfurt)", "lat": 49.8, "lon": 11.0}
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {
        "Active Search": {
            "StepStone TalentFinder": [{"start_date": "2024-01-01", "cost_pa": 1800.0}],
            "LinkedIn Recruiter": [{"start_date": "2024-01-01", "cost_pa": 2400.0}],
            "Xing": [{"start_date": "2024-01-01", "cost_pa": 0.0}]
        },
        "Stellenschaltung": {
            "StepStone": [{"start_date": "2024-01-01", "cost_pa": 4500.0}],
            "LinkedIn Jobs": [{"start_date": "2024-01-01", "cost_pa": 3000.0}],
            "Website": [{"start_date": "2024-01-01", "cost_pa": 0.0}]
        }
    }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE, dtype={'PLZ': str})
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.date
        df['Einstellungsdatum'] = pd.to_datetime(df['Einstellungsdatum'], errors='coerce').dt.date
        return df
    return pd.DataFrame(columns=["ID", "Datum", "Kategorie", "Kanal", "Name", "Vorname", "Job", "Status", "Absagegrund", "PLZ", "Einstellungsdatum"])

def save_data(df_to_save):
    df_to_save.to_csv(DB_FILE, index=False)

def get_coords(plz):
    plz_s = str(plz).zfill(5)
    prefix = plz_s[0]
    return GEO_REGIONS.get(prefix, {"name": "Zentrale", "lat": 51.16, "lon": 10.45})

def calculate_period_cost(cat, channel, start_d, end_d):
    total = 0.0
    history = st.session_state.budget_config.get(cat, {}).get(channel, [])
    sorted_history = sorted(history, key=lambda x: x['start_date'])
    current = start_d
    while current <= end_d:
        price = 0.0
        for entry in sorted_history:
            if current >= datetime.datetime.strptime(entry['start_date'], "%Y-%m-%d").date():
                price = entry['cost_pa']
        total += price / 365.25
        current += datetime.timedelta(days=1)
    return total

# --- INITIALISIERUNG ---
if 'budget_config' not in st.session_state:
    st.session_state.budget_config = load_settings()
df = load_data()

# --- 2. SIDEBAR & ADMIN ---
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    else:
        st.title("🎯 RF-CRM Pro")
    
    st.divider()
    page = st.radio("Navigation", ["📈 Management-Report", "🏃 Operative Pipeline", "⚙️ Einstellungen"])
    
    st.divider()
    st.subheader("🛠️ Demo-Steuerung")
    
    if st.button("🚀 300 Testdaten (smart)"):
        new_data = []
        stages_config = {"Kontaktiert": 148, "Antwort erhalten": 40, "Absage": 80, "Eingestellt": 32}
        reasons_base = ["Gehalt", "Fachliche Qualifikation", "Umzugsbereitschaft", "Anderes Angebot", "keine Reisebereitschaft", "Sonstiges"]
        
        id_counter = 1
        for status, count in stages_config.items():
            for _ in range(count):
                plz_prefix = random.choice(list(GEO_REGIONS.keys()))
                plz = f"{plz_prefix}{random.randint(1000, 9999)}"
                
                # Datumssimulation
                contact_date = datetime.date.today() - datetime.timedelta(days=random.randint(30, 200))
                e_date = None
                reason = "-"
                
                if status == "Absage":
                    if plz_prefix in ["0", "1", "9"]: # OST
                        reason = random.choices(["keine Reisebereitschaft", "Fachliche Qualifikation"], weights=[0.8, 0.2])[0]
                    elif plz_prefix in ["7", "8"]: # SÜD
                        reason = random.choices(["Gehalt", "Sonstiges"], weights=[0.8, 0.2])[0]
                    elif plz_prefix in ["2"]: # NORD
                        reason = random.choices(["Anderes Angebot", "Gehalt"], weights=[0.8, 0.2])[0]
                    else:
                        reason = random.choice(reasons_base)
                
                if status == "Eingestellt":
                    e_date = contact_date + datetime.timedelta(days=random.randint(15, 65))

                new_data.append({
                    "ID": id_counter, "Datum": contact_date, 
                    "Kategorie": random.choice(["Active Search", "Stellenschaltung"]),
                    "Kanal": random.choice(["StepStone", "LinkedIn", "Xing", "Website"]), 
                    "Name": f"Muster{id_counter}", "Vorname": "Kandidat",
                    "Job": random.choice(["Monteur", "Bauleiter", "Projektleiter"]), 
                    "Status": status, "PLZ": plz, "Absagegrund": reason, "Einstellungsdatum": e_date
                })
                id_counter += 1
        df = pd.DataFrame(new_data)
        save_data(df)
        st.success("300 Datensätze geladen!")
        st.rerun()

    if st.button("🗑️ Alle Daten löschen"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        df = pd.DataFrame(columns=["ID", "Datum", "Kategorie", "Kanal", "Name", "Vorname", "Job", "Status", "Absagegrund", "PLZ", "Einstellungsdatum"])
        save_data(df)
        st.rerun()

    st.divider()
    date_input = st.date_input("Filterzeitraum", value=(df['Datum'].min() if not df.empty else datetime.date.today(), datetime.date.today()))

# --- DATENFILTERUNG ---
if isinstance(date_input, tuple) and len(date_input) == 2:
    start_date, end_date = date_input
    f_df = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
else:
    f_df, start_date, end_date = df, datetime.date.today(), datetime.date.today()

# --- 3. MANAGEMENT REPORT ---
if page == "📈 Management-Report":
    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, use_container_width=True)
        else: st.markdown("<h1 style='text-align: center;'>🎯</h1>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; margin-top: -20px;'>Executive Summary</h1>", unsafe_allow_html=True)
    
    if f_df.empty:
        st.info("Datenbank leer. Bitte Daten generieren oder manuell erfassen.")
    else:
        # Kennzahlen-Logik
        report_list = []
        total_hires = 0
        total_days = 0

        for cat, channels in st.session_state.budget_config.items():
            for ch in channels:
                cost = calculate_period_cost(cat, ch, start_date, end_date)
                ch_df = f_df[f_df['Kanal'] == ch]
                hires_in_ch = ch_df[ch_df['Status'] == "Eingestellt"]
                num_hires = len(hires_in_ch)
                
                tth_val = 0
                if num_hires > 0:
                    hires_in_ch['Datum'] = pd.to_datetime(hires_in_ch['Datum'])
                    hires_in_ch['Einstellungsdatum'] = pd.to_datetime(hires_in_ch['Einstellungsdatum'])
                    diffs = (hires_in_ch['Einstellungsdatum'] - hires_in_ch['Datum']).dt.days
                    tth_val = diffs.mean()
                    total_days += diffs.sum()
                    total_hires += num_hires
                
                report_list.append({
                    "Kategorie": cat, "Kanal": ch, "Kosten": cost, "Hires": num_hires, 
                    "Bewerber": len(ch_df), "CPH": (cost/num_hires if num_hires > 0 else 0),
                    "TTH": round(tth_val, 1)
                })

        perf_df = pd.DataFrame(report_list)
        avg_cph = perf_df['Kosten'].sum() / total_hires if total_hires > 0 else 0
        avg_tth = total_days / total_hires if total_hires > 0 else 0

        # KPI DASHBOARD
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Budget", f"{perf_df['Kosten'].sum():,.0f} €")
        m2.metric("Hires", int(total_hires))
        m3.metric("Ø CPH", f"{avg_cph:,.0f} €")
        m4.metric("Ø TTH", f"{avg_tth:.1f} d")
        m5.metric("Bewerber", len(f_df))

        st.divider()
        # NEUES CHART: Status-Verteilung
        st.subheader("📊 Pipeline-Durchlauf (Status-Anzahl)")
        st_order = ["Kontaktiert", "Antwort erhalten", "Interview", "Angebot", "Eingestellt", "Absage"]
        st_counts = f_df['Status'].value_counts().reindex(st_order).fillna(0).reset_index()
        st_counts.columns = ['Status', 'Anzahl']
        fig_st = px.bar(st_counts, x='Status', y='Anzahl', text='Anzahl', color='Status', 
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_st.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_st, use_container_width=True)

        st.divider()
        # GEO-MAP
        st.subheader("🗺️ Regionale Absage-Hotspots")
        abs_df = f_df[f_df['Status'] == "Absage"].copy()
        if not abs_df.empty:
            abs_df['lat'] = abs_df['PLZ'].apply(lambda x: get_coords(x)['lat'])
            abs_df['lon'] = abs_df['PLZ'].apply(lambda x: get_coords(x)['lon'])
            abs_df['PLZ_1'] = abs_df['PLZ'].apply(lambda x: str(x).zfill(5)[0])
            map_data = abs_df.groupby(['PLZ_1', 'Absagegrund', 'lat', 'lon']).size().reset_index(name='Anzahl')
            fig_map = px.scatter_geo(map_data, lat="lat", lon="lon", size="Anzahl", color="Absagegrund", scope='europe')
            fig_map.update_geos(lataxis_range=[47, 55], lonaxis_range=[5, 16], showland=True, showcountries=True)
            st.plotly_chart(fig_map, use_container_width=True)

        st.divider()
        # CPH & TTH Charts
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("🎯 Cost-per-Hire")
            st.plotly_chart(px.bar(perf_df, x="Kanal", y="CPH", color="Kategorie"), use_container_width=True)
        with c_right:
            st.subheader("⏱️ Time-to-Hire")
            st.plotly_chart(px.bar(perf_df, x="Kanal", y="TTH", color="Kategorie"), use_container_width=True)

        st.divider()
        st.subheader("📋 Performance-Tabelle")
        st.table(perf_df.style.format({"Kosten": "{:,.2f} €", "CPH": "{:,.2f} €"}))

# --- 4. OPERATIVE PIPELINE ---
elif page == "🏃 Operative Pipeline":
    st.title("🏃 Kandidaten-Management")
    with st.expander("➕ Neuen Kandidaten hinzufügen"):
        with st.form("new_cand"):
            c1, c2, c3 = st.columns(3)
            vn, nn = c1.text_input("Vorname"), c2.text_input("Nachname")
            plz_in = c3.text_input("PLZ", value="10115")
            cat_sel = st.radio("Strategie", ["Active Search", "Stellenschaltung"], horizontal=True)
            ch_sel = st.selectbox("Kanal", list(st.session_state.budget_config[cat_sel].keys()))
            if st.form_submit_button("Speichern"):
                nid = df['ID'].max()+1 if not df.empty else 1
                new_r = pd.DataFrame([{"ID": nid, "Datum": datetime.date.today(), "Kategorie": cat_sel, "Kanal": ch_sel, "Name": nn, "Vorname": vn, "Job": "Kandidat", "Status": "Kontaktiert", "Absagegrund": "-", "PLZ": plz_in, "Einstellungsdatum": None}])
                df = pd.concat([df, new_r], ignore_index=True)
                save_data(df); st.rerun()

    st_order = ["Kontaktiert", "Antwort erhalten", "Interview", "Angebot", "Eingestellt", "Absage"]
    for phase in st_order:
        pdf = f_df[f_df['Status'] == phase]
        with st.expander(f"**{phase.upper()}** ({len(pdf)})"):
            for _, p in pdf.head(15).iterrows():
                with st.container(border=True):
                    cl1, cl2, cl3 = st.columns([3, 2, 2])
                    cl1.write(f"**{p['Vorname']} {p['Name']}** (Eingang: {p['Datum']})")
                    new_s = cl2.selectbox("Status", st_order, index=st_order.index(p['Status']), key=f"s_{p['ID']}")
                    if new_s == "Absage":
                        reasons = ["Gehalt", "Fachliche Qualifikation", "Umzugsbereitschaft", "Anderes Angebot", "keine Reisebereitschaft", "Sonstiges"]
                        new_re = cl3.selectbox("Grund", reasons, key=f"r_{p['ID']}")
                        if cl3.button("Sichern", key=f"b_{p['ID']}"):
                            df.loc[df['ID'] == p['ID'], 'Status'] = "Absage"
                            df.loc[df['ID'] == p['ID'], 'Absagegrund'] = new_re
                            save_data(df); st.rerun()
                    elif new_s != p['Status']:
                        df.loc[df['ID'] == p['ID'], 'Status'] = new_s
                        df.loc[df['ID'] == p['ID'], 'Einstellungsdatum'] = datetime.date.today() if new_s == "Eingestellt" else None
                        save_data(df); st.rerun()

# --- 5. EINSTELLUNGEN ---
elif page == "⚙️ Einstellungen":
    st.title("⚙️ Budget")
    for cat, channels in st.session_state.budget_config.items():
        st.subheader(cat)
        for ch, hist in channels.items():
            val = st.number_input(f"Kosten p.a. {ch}", value=float(hist[-1]['cost_pa']), key=f"c_{ch}")
            if st.button(f"Update {ch}"):
                st.session_state.budget_config[cat][ch].append({"start_date": "2024-01-01", "cost_pa": val})
                save_settings(st.session_state.budget_config); st.success("Gespeichert")