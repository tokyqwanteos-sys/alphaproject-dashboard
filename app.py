import streamlit as st
import pandas as pd

# 1. CONFIGURATION & DESIGN DYNAMIQUE (TOUJOURS EN PREMIER)
st.set_page_config(page_title="AlphaProject | Master Dashboard", layout="wide", page_icon="🛡️")

# --- GESTION DE L'AUTHENTIFICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    
if 'dashboard_type' not in st.session_state:
    st.session_state.dashboard_type = "TL SETUP"

# --- INTERFACE DE LOGIN ---
if not st.session_state.authenticated:
    st.markdown("""
        <div style='text-align: center; margin-top: 100px; margin-bottom: 50px;'>
            <h1 style='font-family: sans-serif; color: #0ea5e9; font-size: 3rem; font-weight: 800;'>🛡️ AlphaProject</h1>
            <p style='color: #64748B; font-size: 1.2rem;'>Accès sécurisé au Master Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Connexion Administrateur")
            username = st.text_input("👤 Utilisateur", placeholder="Entrez votre identifiant")
            password = st.text_input("🔑 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                if username == "AlphaProject" and password == "Alpha2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects. Accès refusé.")
    
    st.stop()

# --- SI AUTHENTIFIÉ, AFFICHER LE DASHBOARD ---

# --- AJOUT LOGO (LIEN WEB) ET SIGNATURE DANS LA SIDEBAR ---
with st.sidebar:
    logo_url = "https://image2url.com/r2/default/images/1775131743507-3e439d6b-9a7e-4a24-be34-477b9b6f6fee.png"
    st.image(logo_url, use_container_width=True)
    
    st.markdown(f"""
        <div style="text-align: center; margin-top: -15px; margin-bottom: 20px;">
            <h3 style="color: #0ea5e9; font-family: sans-serif; letter-spacing: 2px;">{st.session_state.dashboard_type}</h3>
            <p style="font-size: 0.8em; opacity: 0.7;">AlphaProject Solutions</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(14,165,233,0.75), rgba(0,0,0,0));">
        </div>
    """, unsafe_allow_html=True)
    
    # Sélecteur de dashboard
    st.markdown("### 📊 Navigation")
    dashboard_option = st.radio(
        "Choisir le Dashboard",
        ["TL SETUP", "Match & Prod Setup"],
        index=0 if st.session_state.dashboard_type == "TL SETUP" else 1
    )
    
    if dashboard_option == "TL SETUP" and st.session_state.dashboard_type != "TL SETUP":
        st.session_state.dashboard_type = "TL SETUP"
        st.rerun()
    elif dashboard_option == "Match & Prod Setup" and st.session_state.dashboard_type != "Match & Prod Setup":
        st.session_state.dashboard_type = "Match & Prod Setup"
        st.rerun()
    
    # Bouton de déconnexion
    st.markdown("---")
    if st.button("🚪 Se déconnecter", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# CSS Adaptatif Premium
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(14,165,233,0.12) 0%, rgba(14,165,233,0.04) 100%);
        border: 1px solid rgba(14,165,233,0.25);
        border-radius: 20px;
        padding: 24px 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(14,165,233,0.2);
        border-color: rgba(14,165,233,0.6);
        background: linear-gradient(135deg, rgba(14,165,233,0.18) 0%, rgba(14,165,233,0.08) 100%);
    }
    div[data-testid="stMetric"] label {
        font-weight: 700 !important;
        color: #0ea5e9 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] .stMetricValue {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1E293B !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { 
        font-weight: 600;
        padding: 10px 24px;
        border-radius: 12px;
        transition: all 0.2s;
        background-color: rgba(14,165,233,0.05);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(14,165,233,0.15);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white !important;
    }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #0ea5e9;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD 1: TL SETUP (100% INCHANGÉ)
# ============================================
if st.session_state.dashboard_type == "TL SETUP":
    BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9CwN6tKKroOoWtWwdtFAxhgqW1wMyUg0lrmU8eGtfyR1lSSVZOyg5siuxO9XkUf6WQxeeZ_IGc2uy/pub?single=true&output=csv&gid="

    AGENTS = {
        "Vanja": f"{BASE_URL}225155468",
        "Jy N Aina": f"{BASE_URL}1253872710",
        "Ny Haingo": f"{BASE_URL}919025018",
        "Isaia": f"{BASE_URL}913015590",
        "Toky": f"{BASE_URL}770981752",
        "Zara": f"{BASE_URL}718675776"
    }

    START_ROWS = {
        "Vanja": 8,
        "Jy N Aina": 541,
        "Ny Haingo": 752,
        "Isaia": 702,
        "Toky": 435,
        "Zara": 424
    }

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
    def load_data(url, start_row):
        try:
            df = pd.read_csv(url, header=None, skiprows=start_row-1)
            df.columns = ['Start', 'Pause', 'Reprise', 'Fin', 'DATE', 'Matchs', 'League', 'Tâches', 'Statuts', 'Total', 'BreakTime', 'REMARQUES']
            df['DATE_DT'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
            df['Total_Sec'] = df['Total'].apply(convert_to_seconds)
            return df
        except:
            return pd.DataFrame()

    st.markdown("""
        <div style='text-align: left; margin-bottom: 30px; border-left: 8px solid #0ea5e9; padding-left: 15px;'>
            <h1 style='font-family: sans-serif; color: #1E293B; font-size: 2.2rem; margin: 0; font-weight: 800;'>🛡️ AlphaProject</h1>
            <p style='color: #64748B; font-size: 1.1rem; margin: 0; font-weight: 500;'>Master Dashboard | Suivi & Performance Setup</p>
        </div>
    """, unsafe_allow_html=True)

    all_data = []
    for name, url in AGENTS.items():
        start_row = START_ROWS[name]
        temp_df = load_data(url, start_row)
        if not temp_df.empty:
            temp_df['Agent_Name'] = name
            all_data.append(temp_df)

    if all_data:
        df_global_raw = pd.concat(all_data)
        df_global_valid = df_global_raw[df_global_raw['DATE_DT'].notna() & df_global_raw['Total_Sec'].notna()].copy()

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

        t_master, t_taches, t1, t2, t3 = st.tabs(["🏆 Résumé Agents", "📋 Résumé Tâches", "📊 Détails Tâches", "📈 Charge Journalière", "🔬 Audit Qualité"])

        with t_master:
            total_s_eq = df_filtered['Total_Sec'].sum()
            st.subheader("🏁 Performance Comparative de l'Équipe")
            
            c_g1, c_g2 = st.columns(2)
            c_g1.metric("Volume Total Équipe", format_seconds_to_hms(total_s_eq))
            c_g2.metric("Total Setups", f"{len(df_filtered)}")
            
            summary = df_filtered.groupby('Agent_Name')['Total_Sec'].agg(['sum', 'mean', 'max', 'min', 'count'])
            summary['Prod (U/h)'] = (summary['count'] / (summary['sum'] / 3600)).round(2)
            summary['Temps Total'] = summary['sum'].apply(format_seconds_to_hms)
            summary['Moyenne'] = summary['mean'].apply(format_seconds_to_hms)
            summary['Max'] = summary['max'].apply(format_seconds_to_hms)
            summary['Min'] = summary['min'].apply(format_seconds_to_hms)
            
            summary = summary.rename(columns={'count': 'Nombre de tâches'}).sort_values(by='Nombre de tâches', ascending=False)
            
            display_summary = summary.copy()
            display_summary['Nombre de tâches'] = display_summary['Nombre de tâches'].apply(lambda x: f"{int(x)}")
            display_summary['Prod (U/h)'] = display_summary['Prod (U/h)'].apply(lambda x: f"{x:.2f}")
            
            st.dataframe(display_summary[['Nombre de tâches', 'Temps Total', 'Moyenne', 'Max', 'Min', 'Prod (U/h)']], use_container_width=True)
            
            col_c1, col_c2 = st.columns(2)
            with col_c1: st.bar_chart(summary['Nombre de tâches'], color="#0ea5e9")
            with col_c2: st.bar_chart(summary['Prod (U/h)'], color="#0284c7")

        with t_taches:
            total_s_eq = df_filtered['Total_Sec'].sum()
            st.subheader("📋 Résumé des Tâches - Performance par Type")
            
            c_g1, c_g2 = st.columns(2)
            c_g1.metric("Volume Total Équipe", format_seconds_to_hms(total_s_eq))
            c_g2.metric("Total Setups", f"{len(df_filtered)}")
            
            task_summary = df_filtered.groupby('Tâches')['Total_Sec'].agg(['sum', 'mean', 'max', 'min', 'count'])
            task_summary['Prod (U/h)'] = (task_summary['count'] / (task_summary['sum'] / 3600)).round(2)
            task_summary['Temps Total'] = task_summary['sum'].apply(format_seconds_to_hms)
            task_summary['Moyenne'] = task_summary['mean'].apply(format_seconds_to_hms)
            task_summary['Max'] = task_summary['max'].apply(format_seconds_to_hms)
            task_summary['Min'] = task_summary['min'].apply(format_seconds_to_hms)
            
            task_summary = task_summary.rename(columns={'count': 'Nombre de tâches'}).sort_values(by='Nombre de tâches', ascending=False)
            
            display_task_summary = task_summary.copy()
            display_task_summary['Nombre de tâches'] = display_task_summary['Nombre de tâches'].apply(lambda x: f"{int(x)}")
            display_task_summary['Prod (U/h)'] = display_task_summary['Prod (U/h)'].apply(lambda x: f"{x:.2f}")
            
            st.dataframe(display_task_summary[['Nombre de tâches', 'Temps Total', 'Moyenne', 'Max', 'Min', 'Prod (U/h)']], use_container_width=True)
            
            col_t1, col_t2 = st.columns(2)
            with col_t1: st.bar_chart(task_summary['Nombre de tâches'], color="#0ea5e9")
            with col_t2: st.bar_chart(task_summary['Prod (U/h)'], color="#0284c7")

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
                    display_st_df = st_df.copy()
                    display_st_df['count'] = display_st_df['count'].apply(lambda x: f"{int(x)}")
                    st.dataframe(display_st_df[['Moyenne', 'Total', 'Max', 'Min', 'count']], use_container_width=True)

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

# ============================================
# DASHBOARD 2: MATCH & PROD SETUP (PREMIUM)
# ============================================
elif st.session_state.dashboard_type == "Match & Prod Setup":
    st.markdown("""
        <div style='text-align: left; margin-bottom: 30px; border-left: 8px solid #0ea5e9; padding-left: 15px;'>
            <h1 style='font-family: sans-serif; color: #1E293B; font-size: 2.2rem; margin: 0; font-weight: 800;'>🎯 Match & Prod Setup</h1>
            <p style='color: #64748B; font-size: 1.1rem; margin: 0; font-weight: 500;'>Suivi des Matchs et Mises en Production | Analytics Premium</p>
        </div>
    """, unsafe_allow_html=True)
    
    MATCH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRTXy8AtQMhFzGY-dEE1PrRKgKWaOfmBygmYgIFfJhpL4ivwo8djT1tfgRRyixprh5A858Gl4a8qdYH/pub?gid=225910839&single=true&output=csv"
    PROD_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRTXy8AtQMhFzGY-dEE1PrRKgKWaOfmBygmYgIFfJhpL4ivwo8djT1tfgRRyixprh5A858Gl4a8qdYH/pub?gid=2106899222&single=true&output=csv"
    
    def format_duration(seconds):
        if pd.isna(seconds) or seconds <= 0:
            return "0:00:00"
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h}:{m:02d}:{s:02d}"
    
    @st.cache_data(ttl=60)
    def load_data_optimized(url, start_row):
        try:
            df = pd.read_csv(url, header=None, skiprows=start_row-1, usecols=[4, 6, 8, 11])
            df.columns = ['DATE', 'Agent', 'Durée', 'REMARQUES']
            df['DATE_DT'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
            
            def convert_duration(dur):
                try:
                    if pd.isna(dur) or str(dur).strip() == "":
                        return 0.0
                    parts = str(dur).strip().split(':')
                    if len(parts) == 3:
                        return int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
                    elif len(parts) == 2:
                        return int(parts[0])*60 + int(parts[1])
                    return 0.0
                except:
                    return 0.0
            
            df['Durée_Sec'] = df['Durée'].apply(convert_duration)
            return df
        except Exception as e:
            return pd.DataFrame()
    
    # Chargement des données
    df_match = load_data_optimized(MATCH_URL, 2467)
    df_prod = load_data_optimized(PROD_URL, 1014)
    
    # Filtre date unique pour les deux feuilles
    all_dates = []
    if not df_match.empty:
        all_dates.extend(df_match['DATE_DT'].dropna().tolist())
    if not df_prod.empty:
        all_dates.extend(df_prod['DATE_DT'].dropna().tolist())
    
    if all_dates:
        min_date = min(all_dates).date()
        max_date = max(all_dates).date()
        
        st.sidebar.markdown("### 📅 Filtre Temporel Global")
        date_range = st.sidebar.date_input("Période d'analyse", value=(min_date, max_date))
        
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date, end_date = None, None
        st.sidebar.warning("⚠️ Aucune donnée chargée")
    
    # Application du filtre unique
    if not df_match.empty and start_date and end_date:
        df_match_filtered = df_match[(df_match['DATE_DT'].dt.date >= start_date) & (df_match['DATE_DT'].dt.date <= end_date)]
    else:
        df_match_filtered = df_match.copy() if not df_match.empty else pd.DataFrame()
    
    if not df_prod.empty and start_date and end_date:
        df_prod_filtered = df_prod[(df_prod['DATE_DT'].dt.date >= start_date) & (df_prod['DATE_DT'].dt.date <= end_date)]
    else:
        df_prod_filtered = df_prod.copy() if not df_prod.empty else pd.DataFrame()
    
    # Onglets: Résumé Global et Résumé par Type
    t_summary, t_match, t_prod = st.tabs(["📊 Résumé Global", "🎯 Analyse Match", "🚀 Analyse Production"])
    
    with t_summary:
        st.subheader("📊 Tableau de Bord Exécutif")
        
        # Métriques globales
        col1, col2, col3, col4 = st.columns(4)
        
        total_match = len(df_match_filtered)
        total_prod = len(df_prod_filtered)
        total_operations = total_match + total_prod
        
        with col1:
            st.metric("📊 Total Opérations", f"{total_operations:,}", delta=f"Match: {total_match} | Prod: {total_prod}")
        with col2:
            duree_match = df_match_filtered['Durée_Sec'].sum() if not df_match_filtered.empty else 0
            duree_prod = df_prod_filtered['Durée_Sec'].sum() if not df_prod_filtered.empty else 0
            st.metric("⏱️ Volume Total", format_duration(duree_match + duree_prod))
        with col3:
            avg_duree = (duree_match + duree_prod) / total_operations if total_operations > 0 else 0
            st.metric("📊 Durée Moyenne", format_duration(avg_duree))
        with col4:
            agents_match = df_match_filtered['Agent'].nunique() if not df_match_filtered.empty else 0
            agents_prod = df_prod_filtered['Agent'].nunique() if not df_prod_filtered.empty else 0
            st.metric("👥 Équipe engagée", max(agents_match, agents_prod))
        
        st.markdown("---")
        
        # Graphiques comparatifs
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 📈 Évolution Match")
            if not df_match_filtered.empty:
                daily_match = df_match_filtered.groupby('DATE_DT').size()
                st.line_chart(daily_match, color="#0ea5e9", height=300)
                st.caption(f"Période: {start_date} → {end_date} | Total: {total_match} opérations")
            else:
                st.info("Aucune donnée Match sur cette période")
        
        with col_chart2:
            st.markdown("### 📈 Évolution Production")
            if not df_prod_filtered.empty:
                daily_prod = df_prod_filtered.groupby('DATE_DT').size()
                st.line_chart(daily_prod, color="#0284c7", height=300)
                st.caption(f"Période: {start_date} → {end_date} | Total: {total_prod} opérations")
            else:
                st.info("Aucune donnée Production sur cette période")
        
        st.markdown("---")
        
        # Top Performers
        st.subheader("🏆 Top Performers")
        
        col_perf1, col_perf2 = st.columns(2)
        
        with col_perf1:
            st.markdown("**🎯 Match Setup**")
            if not df_match_filtered.empty:
                top_match = df_match_filtered.groupby('Agent').size().sort_values(ascending=False).head(5)
                for agent, count in top_match.items():
                    st.markdown(f"- **{agent}** : {count} opérations")
            else:
                st.info("Aucune donnée")
        
        with col_perf2:
            st.markdown("**🚀 Mis en Prod Setup**")
            if not df_prod_filtered.empty:
                top_prod = df_prod_filtered.groupby('Agent').size().sort_values(ascending=False).head(5)
                for agent, count in top_prod.items():
                    st.markdown(f"- **{agent}** : {count} opérations")
            else:
                st.info("Aucune donnée")
    
    with t_match:
        st.subheader("🎯 Analyse Détaillée - Match Setup")
        
        if not df_match_filtered.empty:
            # Métriques
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("📦 Total Matchs", f"{len(df_match_filtered):,}")
            with col_b:
                st.metric("⏱️ Durée Totale", format_duration(df_match_filtered['Durée_Sec'].sum()))
            with col_c:
                st.metric("📊 Durée Moyenne", format_duration(df_match_filtered['Durée_Sec'].mean()))
            with col_d:
                st.metric("👥 Agents Actifs", df_match_filtered['Agent'].nunique())
            
            # Performance par agent
            st.subheader("📊 Performance par Agent")
            agent_stats = df_match_filtered.groupby('Agent')['Durée_Sec'].agg(['count', 'sum', 'mean']).round(2)
            agent_stats['Durée Totale'] = agent_stats['sum'].apply(format_duration)
            agent_stats['Durée Moyenne'] = agent_stats['mean'].apply(format_duration)
            agent_stats = agent_stats.rename(columns={'count': 'Nombre'})
            agent_stats = agent_stats.sort_values('Nombre', ascending=False)
            st.dataframe(agent_stats[['Nombre', 'Durée Totale', 'Durée Moyenne']], use_container_width=True)
            
            # Détails
            with st.expander("📋 Tous les logs Match", expanded=False):
                display_df = df_match_filtered.drop(columns=['DATE_DT', 'Durée_Sec'])
                st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.info("Aucune donnée Match disponible sur cette période")
    
    with t_prod:
        st.subheader("🚀 Analyse Détaillée - Mis en Prod Setup")
        
        if not df_prod_filtered.empty:
            # Métriques
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("📦 Total Productions", f"{len(df_prod_filtered):,}")
            with col_b:
                st.metric("⏱️ Durée Totale", format_duration(df_prod_filtered['Durée_Sec'].sum()))
            with col_c:
                st.metric("📊 Durée Moyenne", format_duration(df_prod_filtered['Durée_Sec'].mean()))
            with col_d:
                st.metric("👥 Agents Actifs", df_prod_filtered['Agent'].nunique())
            
            # Performance par agent
            st.subheader("📊 Performance par Agent")
            agent_stats = df_prod_filtered.groupby('Agent')['Durée_Sec'].agg(['count', 'sum', 'mean']).round(2)
            agent_stats['Durée Totale'] = agent_stats['sum'].apply(format_duration)
            agent_stats['Durée Moyenne'] = agent_stats['mean'].apply(format_duration)
            agent_stats = agent_stats.rename(columns={'count': 'Nombre'})
            agent_stats = agent_stats.sort_values('Nombre', ascending=False)
            st.dataframe(agent_stats[['Nombre', 'Durée Totale', 'Durée Moyenne']], use_container_width=True)
            
            # Détails
            with st.expander("📋 Tous les logs Production", expanded=False):
                display_df = df_prod_filtered.drop(columns=['DATE_DT', 'Durée_Sec'])
                st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.info("Aucune donnée Production disponible sur cette période")
