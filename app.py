import streamlit as st
import pandas as pd
import base64

# 1. CONFIGURATION & DESIGN DYNAMIQUE
st.set_page_config(page_title="AlphaProject | Master Dashboard", layout="wide", page_icon="🛡️")

# --- AJOUT LOGO ET SIGNATURE DANS LA SIDEBAR (HAUT À GAUCHE) ---
with st.sidebar:
    # Encodage de l'image locale pour l'affichage
    try:
        with open("téléchargement.png", "rb") as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
        st.image(f"data:image/png;base64,{bin_str}", use_container_width=True)
    except:
        st.error("Logo introuvable (téléchargement.png)")
    
    # Signature stylisée
    st.markdown("""
        <div style="text-align: center; margin-top: -15px; margin-bottom: 20px;">
            <h3 style="color: #0ea5e9; font-family: sans-serif; letter-spacing: 2px;">TL SETUP</h3>
            <p style="font-size: 0.8em; opacity: 0.7;">AlphaProject Solutions</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(14,165,233,0.75), rgba(0,0,0,0));">
        </div>
    """, unsafe_allow_html=True)

# CSS Adaptatif
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #0ea5e9;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    .stApp { transition: background-color 0.3s ease; }
    </style>
    """, unsafe_allow_html=True)

# 2. RÉPERTOIRE DES AGENTS
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9CwN6tKKroOoWtWwdtFAxhgqW1wMyUg0lrmU8eGtfyR1lSSVZOyg5siuxO9XkUf6WQxeeZ_IGc2uy/pub?single=true&output=csv&gid="

AGENTS = {
    "Vanja": f"{BASE_URL}225155468",
    "Jy N Aina": f"{BASE_URL}1253872710",
    "Ny Haingo": f"{BASE_URL}919025018",
    "Isaia": f"{BASE_URL}913015590",
    "Toky": f"{BASE_URL}770981752",
    "Zara": f"{BASE_URL}718675776"
}

# 3. MOTEURS DE CALCUL
def convert_to_seconds(time_val):
    try:
        if pd.isna(time_val) or str(time_val).strip() in ["", "0", "0:00:00"]: return 0.0
        parts = str(time_val).strip().split(':')
        if len(parts) == 3: return int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
        elif len(parts) == 2: return int(parts[0])*60 + int(parts[1])
        return 0.0
    except: return None

def format_seconds_to_hms(seconds):
    if pd.isna(seconds) or seconds <= 0: return "0:00:00"
    h, m = divmod(int(seconds), 3600)
    m, s = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url, header=None, skiprows=7)
        df.columns = ['Start', 'Pause', 'Reprise', 'Fin', 'DATE', 'Matchs', 'League', 'Tâches', 'Statuts', 'Total', 'BreakTime', 'REMARQUES']
        df['DATE_DT'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
        df['Total_Sec'] = df['Total'].apply(convert_to_seconds)
        return df
    except:
        return pd.DataFrame()

# 4. LOGIQUE PRINCIPALE
st.title("🛡️ AlphaProject : Suivi Setup")

all_data = []
for name, url in AGENTS.items():
    temp_df = load_data(url)
    if not temp_df.empty:
        temp_df['Agent_Name'] = name
        all_data.append(temp_df)

if all_data:
    df_global_raw = pd.concat(all_data)
    df_global_valid = df_global_raw[df_global_raw['DATE_DT'].notna() & df_global_raw['Total_Sec'].notna()].copy()

    # SIDEBAR SUITE
    st.sidebar.markdown("### 📅 Filtre Temporel")
    min_d, max_d = df_global_valid['DATE_DT'].min().date(), df_global_valid['DATE_DT'].max().date()
    date_range = st.sidebar.date_input("Période", value=(min_d, max_d))

    if isinstance(date_range, tuple) and len(date_range) == 2:
        df_filtered = df_global_valid[(df_global_valid['DATE_DT'].dt.date >= date_range[0]) & 
                                     (df_global_valid['DATE_DT'].dt.date <= date_range[1])]
    else:
        df_filtered = df_global_valid

    st.sidebar.markdown("---")
    agent_focus = st.sidebar.selectbox("👤 Focus Individuel", list(AGENTS.keys()))

    # ONGLETS
    t_master, t1, t2, t3 = st.tabs(["🏆 Résumé Agents", "📊 Détails Tâches", "📈 Charge Journalière", "🔬 Audit Qualité"])

    with t_master:
        total_s_eq = df_filtered['Total_Sec'].sum()
        st.subheader("🏁 Performance Comparative de l'Équipe")
        
        c_g1, c_g2 = st.columns(2)
        c_g1.metric("Volume Total Équipe", format_seconds_to_hms(total_s_eq))
        c_g2.metric("Total Setups", f"{len(df_filtered)} unités")
        
        summary = df_filtered.groupby('Agent_Name')['Total_Sec'].agg(['sum', 'mean', 'max', 'min', 'count'])
        summary['Prod (U/h)'] = (summary['count'] / (summary['sum'] / 3600)).round(2)
        summary['Temps Total'] = summary['sum'].apply(format_seconds_to_hms)
        summary['Moyenne'] = summary['mean'].apply(format_seconds_to_hms)
        summary['Max'] = summary['max'].apply(format_seconds_to_hms)
        summary['Min'] = summary['min'].apply(format_seconds_to_hms)
        
        summary = summary.rename(columns={'count': 'Unités'}).sort_values(by='Unités', ascending=False)
        st.dataframe(summary[['Unités', 'Temps Total', 'Moyenne', 'Max', 'Min', 'Prod (U/h)']], use_container_width=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1: st.bar_chart(summary['Unités'], color="#0ea5e9")
        with col_c2: st.bar_chart(summary['Prod (U/h)'], color="#0284c7")

    # FOCUS INDIVIDUEL
    df_agent = df_filtered[df_filtered['Agent_Name'] == agent_focus]
    df_agent_raw = df_global_raw[df_global_raw['Agent_Name'] == agent_focus]
    df_err = df_agent_raw[df_agent_raw['DATE_DT'].isna() & df_agent_raw['Tâches'].notna()]

    with t1:
        st.subheader(f"Statistiques Tâches : {agent_focus}")
        if not df_agent.empty:
            st.info(f"Temps de travail total pour {agent_focus} : {format_seconds_to_hms(df_agent['Total_Sec'].sum())}")
            col_l, col_r = st.columns([1, 2])
            with col_l:
                st.bar_chart(df_agent['Tâches'].value_counts(), color="#38bdf8")
            with col_r:
                st_df = df_agent.groupby('Tâches')['Total_Sec'].agg(['mean', 'sum', 'max', 'min', 'count']).sort_values(by='sum', ascending=False)
                st_df['Moyenne'] = st_df['mean'].apply(format_seconds_to_hms)
                st_df['Total'] = st_df['sum'].apply(format_seconds_to_hms)
                st_df['Max'] = st_df['max'].apply(format_seconds_to_hms)
                st_df['Min'] = st_df['min'].apply(format_seconds_to_hms)
                st.dataframe(st_df[['Moyenne', 'Total', 'Max', 'Min', 'count']], use_container_width=True)

    with t2:
        st.subheader(f"Flux temporel : {agent_focus}")
        if not df_agent.empty:
            st.area_chart(df_agent.groupby('DATE_DT')['Total_Sec'].sum(), color="#0ea5e9")

    with t3:
        st.subheader(f"Audit : {agent_focus}")
        if not df_err.empty:
            st.warning(f"🚨 {len(df_err)} lignes incomplètes.")
            st.table(df_err[['DATE', 'Matchs', 'Tâches', 'Total']])
        else: st.success(f"✅ Audit conforme.")
        with st.expander("Détails des logs"):
            st.dataframe(df_agent.drop(columns=['Agent_Name', 'Total_Sec']), use_container_width=True)
else:
    st.error("Données indisponibles.")