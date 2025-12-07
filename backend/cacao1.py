# streamlit_app.py

import os
import sqlite3
import pandas as pd  # type: ignore
import joblib  # type: ignore
import streamlit as st  # type: ignore
from datetime import date
import plotly.graph_objects as go  # type: ignore
import plotly.express as px  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
import time
from auth_system import auth

# Configuration de la page - DOIT ÊTRE LE PREMIER APPEL STREAMLIT
st.set_page_config(
    page_title="🎯 MON CACAO - IA PRÉDICTIVE", 
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles personnalisés modernes
st.markdown("""
    <style>
        /* Variables CSS pour la cohérence des couleurs */
        :root {
            --primary-color: #2E8B57;
            --secondary-color: #1a472a;
            --accent-color: #FFD700;
            --background-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-primary: #2c3e50;
            --text-secondary: #6c757d;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --border-radius: 12px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        /* Style global */
        .main {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }

        /* Header personnalisé */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
            text-align: center;
            box-shadow: var(--box-shadow);
        }

        /* Style pour la barre latérale */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--secondary-color) 0%, var(--primary-color) 100%) !important;
            padding: 1.5rem 1rem !important;
            border-right: 3px solid var(--accent-color) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        /* Logo et titre de la barre latérale */
        section[data-testid="stSidebar"] .stTitle {
            background: linear-gradient(45deg, var(--accent-color), #FFA500) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-size: 2.5rem !important;
            font-weight: 900 !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
            position: relative !important;
        }

        section[data-testid="stSidebar"] .stTitle::before {
            content: "🌱" !important;
            display: block !important;
            font-size: 3rem !important;
            margin-bottom: 0.5rem !important;
            animation: bounce 2s infinite !important;
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        /* Navigation moderne */
        section[data-testid="stSidebar"] .stSubheader {
            color: var(--accent-color) !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            margin: 2rem 0 1rem 0 !important;
            padding: 0.75rem 1rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            background: rgba(255,255,255,0.1) !important;
            border-radius: var(--border-radius) !important;
            text-align: center !important;
            border: 2px solid var(--accent-color) !important;
            box-shadow: var(--box-shadow) !important;
        }
        
        /* Boutons de navigation modernes */
        section[data-testid="stSidebar"] .stRadio > div {
            background: transparent !important;
            border: none !important;
        }
        
        section[data-testid="stSidebar"] .stRadio label {
            color: white !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            background: rgba(255,255,255,0.1) !important;
            border-radius: var(--border-radius) !important;
            padding: 1rem 1.5rem !important;
            margin: 0.5rem 0 !important;
            transition: var(--transition) !important;
            cursor: pointer !important;
            border: 2px solid transparent !important;
            backdrop-filter: blur(10px) !important;
        }
        
        section[data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(255,255,255,0.2) !important;
            transform: translateX(8px) scale(1.02) !important;
            border-color: var(--accent-color) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
        }
        
        section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
            background: linear-gradient(135deg, var(--accent-color), #FFA500) !important;
            color: var(--secondary-color) !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 8px rgba(255,215,0,0.3) !important;
            border-color: var(--accent-color) !important;
        }

        /* Boutons modernes */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
            color: white !important;
            border-radius: var(--border-radius) !important;
            padding: 1rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
            border: none !important;
            box-shadow: var(--box-shadow) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color)) !important;
        }

        /* Cartes modernes */
        .modern-card {
            background: var(--card-bg) !important;
            border-radius: var(--border-radius) !important;
            padding: 2rem !important;
            box-shadow: var(--box-shadow) !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            transition: var(--transition) !important;
            margin: 1rem 0 !important;
        }

        .modern-card:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        }

        /* Formulaires modernes */
        div[data-testid="stForm"] {
            background: var(--card-bg) !important;
            padding: 2.5rem !important;
            border-radius: var(--border-radius) !important;
            box-shadow: var(--box-shadow) !important;
            margin: 1.5rem 0 !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
        }

        /* Champs de saisie modernes */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] select {
            border-radius: var(--border-radius) !important;
            border: 2px solid #e9ecef !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            transition: var(--transition) !important;
            background: #f8f9fa !important;
        }
        
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stSelectbox"] select:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(46,139,87,0.1) !important;
            background: white !important;
        }

        /* Métriques modernes */
        div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--primary-color) !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }
        
        div[data-testid="stMetricDelta"] {
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }

        /* Onglets modernes */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
            background-color: transparent !important;
            border-bottom: 2px solid #e9ecef !important;
            padding-bottom: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
            border-radius: var(--border-radius) var(--border-radius) 0 0 !important;
            color: var(--text-secondary) !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
            border: 2px solid transparent !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
            color: white !important;
            border-bottom: 3px solid var(--accent-color) !important;
            transform: translateY(-2px) !important;
        }

        /* Titres modernes */
        h1 {
            color: var(--primary-color) !important;
            font-size: 3rem !important;
            font-weight: 900 !important;
            margin-bottom: 2rem !important;
            text-align: center !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        h2 {
            color: var(--secondary-color) !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 !important;
            border-left: 4px solid var(--accent-color) !important;
            padding-left: 1rem !important;
        }
        
        h3 {
            color: var(--text-primary) !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 1rem 0 !important;
        }

        /* Messages d'alerte modernes */
        .stAlert {
            border-radius: var(--border-radius) !important;
            border: none !important;
            box-shadow: var(--box-shadow) !important;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            h1 { font-size: 2rem !important; }
            h2 { font-size: 1.5rem !important; }
            .modern-card { padding: 1.5rem !important; }
        }

        /* Scrollbar personnalisée */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
    </style>
""", unsafe_allow_html=True)

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
BASE_DIR   = os.path.abspath(os.path.dirname(__file__))
DB_PATH    = os.path.join(BASE_DIR, "data.sqlite")
MODEL_PATH = os.path.join(BASE_DIR, "model_productivite_xgb.pkl")

# Données de référence pour les comparaisons
MOYENNES_REGIONALES = {
    "Indenie-Djuablin": {"production": 0.85, "cout": 450000},
    "Yamoussoukro": {"production": 0.75, "cout": 425000},
    "La Me": {"production": 0.80, "cout": 440000},
    "San-Pedro": {"production": 0.90, "cout": 460000},
    "Grand-Ponts": {"production": 0.82, "cout": 445000}
}

# Suggestions d'optimisation
SUGGESTIONS = {
    "production_faible": [
        "✓ Envisagez l'utilisation d'engrais adaptés",
        "✓ Vérifiez l'état sanitaire des plants",
        "✓ Optimisez la densité de plantation"
    ],
    "cout_eleve": [
        "✓ Analysez la répartition des coûts",
        "✓ Optimisez l'utilisation des intrants",
        "✓ Mutualisez certains équipements"
    ],
    "benefice_faible": [
        "✓ Cherchez des circuits de vente plus avantageux",
        "✓ Réduisez les coûts non essentiels",
        "✓ Améliorez la qualité pour de meilleurs prix"
    ]
}

# Charger le modèle XGBoost optimisé
xgb_model = joblib.load(MODEL_PATH)

# ─── INITIALISATION DE LA BD ───────────────────────────────────────────────────
def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Table des utilisateurs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)
    # Table pour stocker les données annuelles soumises
    cur.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        Cout_production REAL,
        Age_verger REAL,
        Region TEXT,
        Niveau_education TEXT,
        Competences TEXT,
        Engrais TEXT,
        Agroforesterie TEXT,
        Fumier TEXT,
        Herbicide TEXT,
        Insecticide TEXT,
        Fongicide TEXT,
        Pluviometrie TEXT,
        Maladie TEXT,
        Sexe TEXT,
        Productivite REAL,
        submitted_at DATE,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)
    con.commit()
    con.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if not os.path.exists(DB_PATH):
    init_db()

# ─── UTILITAIRES D'AUTHENTIFICATION ────────────────────────────────────────────
def register_user(username, password):
    con = get_db_connection()
    hashed = generate_password_hash(password)
    try:
        con.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed),
        )
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def authenticate_user(username, password):
    con = get_db_connection()
    cur = con.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,)
    )
    row = cur.fetchone()
    con.close()
    if row and check_password_hash(row["password_hash"], password):
        return row["id"]
    return None

# ─── SESSION ───────────────────────────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    user_id = authenticate_user(username, password)
    if user_id:
        st.session_state.user_id = user_id
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.user_id = None
    st.session_state.username = ""

# ─── FONCTION BANNIÈRE UNIFORME ───────────────────────────────────────────────
def create_header_banner(page_context=""):
    """Crée une bannière d'en-tête uniforme pour toutes les pages avec contexte spécifique"""
    
    # Déterminer le statut de l'utilisateur
    if st.session_state.user_id is not None:
        status_text = "En ligne"
        status_color = "#28a745"
        user_role = "Agriculteur"
        username = st.session_state.username if hasattr(st.session_state, 'username') else "Utilisateur"
        
        # Déterminer le contexte de la page pour personnaliser la bannière
        page_icon = "🍃"
        page_subtitle = ""
        
        if "Soumettre" in page_context:
            page_icon = "📥"
            page_subtitle = "Soumission de données"
        elif "Historique" in page_context or "Mes données" in page_context:
            page_icon = "📈"
            page_subtitle = "Historique et analyses"
        elif "Analyse" in page_context:
            page_icon = "📊"
            page_subtitle = "Analyse détaillée"
        elif "Assistant" in page_context:
            page_icon = "🤖"
            page_subtitle = "Assistant IA"
        elif "Conseil" in page_context:
            page_icon = "💡"
            page_subtitle = "Conseils personnalisés"
        elif "Admin" in page_context:
            page_icon = "⚙️"
            page_subtitle = "Administration"
        elif "Prédiction" in page_context:
            page_icon = "🎯"
            page_subtitle = "Prédiction IA"
        
        # Bouton de déconnexion avec style amélioré
        logout_button = f"""
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 14px; opacity: 0.9;">👤 {username}</span>
                <button onclick="window.location.href='/?nav=🚪+Déconnexion'" 
                        style="background: linear-gradient(135deg, #28a745, #20c997); 
                               color: white; 
                               border: none; 
                               padding: 10px 18px; 
                               border-radius: 8px; 
                               cursor: pointer; 
                               font-weight: 600; 
                               font-size: 14px;
                               box-shadow: 0 3px 8px rgba(0,0,0,0.15); 
                               display: flex; 
                               align-items: center; 
                               gap: 8px;
                               transition: all 0.3s ease;
                               hover: transform: translateY(-2px);
                               hover: box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                    <span style="font-size: 16px;">→</span>
                    Déconnexion
                </button>
            </div>
        """
    else:
        status_text = "Hors ligne"
        status_color = "#dc3545"
        user_role = "Visiteur"
        page_icon = "🍃"
        page_subtitle = ""
        logout_button = ""
    
    banner_html = f"""
    <div style="
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 20px 25px;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        position: relative;
        overflow: hidden;
    ">
        <!-- Effet de brillance -->
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            animation: shine 3s infinite;
        "></div>
        
        <!-- Logo et titre -->
        <div style="display: flex; align-items: center; gap: 15px; position: relative; z-index: 2;">
            <div style="
                display: flex; 
                align-items: center; 
                gap: 10px; 
                font-size: 26px;
                background: rgba(255,255,255,0.1);
                padding: 8px 12px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
            ">
                <span style="font-size: 30px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🍃</span>
                <span style="font-size: 30px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🪙</span>
            </div>
            <div>
                <h1 style="
                    margin: 0; 
                    font-size: 32px; 
                    font-weight: 800; 
                    color: white;
                    text-shadow: 0 3px 6px rgba(0,0,0,0.3);
                    letter-spacing: 1px;
                ">Mon Cacao</h1>
                <div style="display: flex; align-items: center; gap: 10px; font-size: 15px; margin-top: 6px;">
                    <div style="
                        width: 10px; 
                        height: 10px; 
                        background-color: {status_color}; 
                        border-radius: 50%; 
                        display: inline-block;
                        box-shadow: 0 0 8px {status_color};
                        animation: pulse 2s infinite;
                    "></div>
                    <span style="font-weight: 600;">{status_text}</span>
                    <span style="margin-left: 20px; opacity: 0.9;">👤 {user_role}</span>
                    {f'<span style="margin-left: 20px; opacity: 0.8; font-size: 13px; background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 6px;">{page_icon} {page_subtitle}</span>' if page_subtitle else ''}
                </div>
            </div>
        </div>
        
        <!-- Bouton de déconnexion -->
        <div style="position: relative; z-index: 2;">
            {logout_button}
        </div>
        
        <!-- CSS pour les animations -->
        <style>
            @keyframes shine {{
                0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
                100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.7; transform: scale(1.1); }}
            }}
        </style>
    </div>
    """
    
    st.markdown(banner_html, unsafe_allow_html=True)

# ─── INTERFACE STREAMLIT ──────────────────────────────────────────────────────
# Affichage de la bannière uniforme (sera mise à jour selon la page)
create_header_banner()

st.sidebar.title("Mon Cacao")
st.sidebar.subheader("🔗 Navigation")

allowed_admins = {"admin"}

if st.session_state.user_id is None:
    choice = st.sidebar.radio("Aller à :", ("🔑 Connexion", "📝 Inscription"))
else:
    if st.session_state.username in allowed_admins:
        choice = st.sidebar.radio(
            "Aller à :",
            ("📊 Prédiction", "📥 Soumettre données", "📂 Mes données", "🤖 Assistant IA", "💡 Conseils", "🔒 Admin", "🚪 Déconnexion"),
        )
    else:
        choice = st.sidebar.radio(
            "Aller à :",
            ("📊 Prédiction", "📥 Soumettre données", "📂 Mes données", "🤖 Assistant IA", "💡 Conseils", "🚪 Déconnexion"),
        )

# ─── PAGE INSCRIPTION ─────────────────────────────────────────────────────────
if choice == "📝 Inscription":
    # Création d'une mise en page à trois colonnes pour centrer le contenu
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.title("🎯 INSCRIPTION")
        
        # Container stylisé pour le formulaire d'inscription
        with st.container():
            st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                    <h3 style="color: #2E86AB;">👋 Bienvenue sur Mon Cacao !</h3>
                    <p style="font-size:16px; color:#333;">
                        Créez votre compte pour accéder à toutes les fonctionnalités :
                        <ul>
                            <li>📊 Prédictions de productivité</li>
                            <li>📈 Suivi de vos performances</li>
                            <li>💡 Recommandations personnalisées</li>
                            <li>📱 Tableau de bord interactif</li>
                            <li>🌱 Scores écologiques</li>
                            <li>🤖 Assistant IA personnalisé</li>
                        </ul>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Formulaire d'inscription amélioré
            with st.form("signup_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                new_username = st.text_input("👤 Nom d'utilisateur", 
                                          key="reg_user",
                                              help="Choisissez un nom d'utilisateur unique (3-50 caractères)")
                    
                    new_email = st.text_input("📧 Adresse e-mail", 
                                            key="reg_email",
                                            help="Votre adresse e-mail valide")
                
                new_password = st.text_input("🔒 Mot de passe", 
                                          type="password",
                                          key="reg_pwd",
                                              help="Minimum 8 caractères avec majuscule, minuscule, chiffre et caractère spécial")
                
                with col2:
                    first_name = st.text_input("📝 Prénom", key="reg_first_name")
                    last_name = st.text_input("📝 Nom de famille", key="reg_last_name")
                    region = st.selectbox("🌍 Région de production", [
                        "Abidjan", "San-Pédro", "Gagnoa", "Divo", "Yamoussoukro",
                        "Bouaké", "Korhogo", "Man", "Daloa", "Autre"
                    ], key="reg_region")
                
                # Politique de gestion des données
                st.markdown("---")
                st.markdown("### 📋 Politique de gestion des données")
                
                with st.expander("📖 Lire la politique de gestion des données complète"):
                    try:
                        with open("POLITIQUE_GESTION_DONNEES.md", "r", encoding="utf-8") as f:
                            policy_content = f.read()
                        st.markdown(policy_content)
                    except FileNotFoundError:
                        st.info("📄 Politique de gestion des données en cours de chargement...")
                
                consent_gdpr = st.checkbox(
                    "✅ J'accepte la politique de gestion des données et j'autorise le traitement de mes données personnelles",
                    key="reg_consent",
                    value=False
                )
                
                confirm_password = st.text_input("🔄 Confirmer le mot de passe",
                                              type="password",
                                              key="reg_confirm",
                                              help="Retapez votre mot de passe")
                
                # Bouton d'inscription
                submit = st.form_submit_button("🚀 Créer mon compte", use_container_width=True)
                
                if submit:
                    # Validation des champs
                    if not all([new_username, new_email, new_password, confirm_password]):
                        st.error("⚠️ Tous les champs obligatoires doivent être remplis.")
                    elif len(new_password) < 8:
                        st.error("⚠️ Le mot de passe doit faire au moins 8 caractères.")
                    elif new_password != confirm_password:
                        st.error("⚠️ Les mots de passe ne correspondent pas.")
                    elif not consent_gdpr:
                        st.error("❌ Vous devez accepter la politique de gestion des données.")
                    else:
                        # Utilisation du nouveau système d'authentification
                        success, result = auth.register_user(
                            new_username, new_email, new_password, 
                            first_name, last_name, region
                        )
                        if success:
                            st.success(f"✅ {result}")
                            st.balloons()
                            st.info("🔄 Vous pouvez maintenant vous connecter avec vos identifiants")
                        else:
                            st.error(f"❌ {result}")
            
            # Pied de page
            st.markdown("""
                <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #666;">
                    <p>Déjà inscrit ? <a href="/?nav=🔑+Connexion">Se connecter</a></p>
                    <p>🔒 Vos données sont sécurisées | 🛡️ Protection de la vie privée</p>
                </div>
            """, unsafe_allow_html=True)

# ─── PAGE CONNEXION ───────────────────────────────────────────────────────────
elif choice == "🔑 Connexion":
    # Création d'une mise en page à trois colonnes pour centrer le contenu
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.title("🎯 CONNEXION")
        
        # Container stylisé pour le formulaire de connexion
        with st.container():
            st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                    <h3 style="color: #2E86AB;">👋 Bienvenue sur Mon Cacao</h3>
                    <p style="font-size:16px; color:#333;">
                        Connectez-vous pour accéder à votre espace personnel
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Formulaire de connexion
            with st.form("login_form"):
                uname = st.text_input("👤 Nom d'utilisateur", 
                                    key="login_user",
                                    help="Entrez votre nom d'utilisateur")
                
                pwd = st.text_input("🔒 Mot de passe", 
                                  type="password",
                                  key="login_pwd",
                                  help="Entrez votre mot de passe")
                
                # Case à cocher "Se souvenir de moi"
                remember_me = st.checkbox("Se souvenir de moi", 
                                        help="Cochez cette case pour rester connecté")
                
                # Bouton de connexion
                submit = st.form_submit_button("Se connecter", use_container_width=True)
                
                if submit:
                    if not uname or not pwd:
                        st.error("⚠️ Veuillez remplir tous les champs.")
                    else:
                        # Utilisation du nouveau système d'authentification
                        success, result = auth.login_user(uname, pwd)
                        if success:
                            st.session_state.user_id = result["user_id"]
                            st.session_state.username = result["username"]
                            st.session_state.session_token = result["session_token"]
                            st.session_state.logged_in = True
                            st.success(f"✅ Bienvenue, **{result['username']}** !")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
            
            # Pied de page
            st.markdown("""
                <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #666;">
                    <p>Pas encore inscrit ? <a href="/?nav=📝+Inscription">Créer un compte</a></p>
                    <p>🔒 Connexion sécurisée | 🛡️ Données protégées</p>
                </div>
            """, unsafe_allow_html=True)

# ─── PAGE DÉCONNEXION ──────────────────────────────────────────────────────────
elif choice == "🚪 Déconnexion" and st.session_state.user_id is not None:
    # Utilisation du nouveau système d'authentification
    if "session_token" in st.session_state:
        auth.logout_user(st.session_state.session_token)
    
    # Nettoyage de la session
    for key in ["user_id", "username", "session_token", "logged_in"]:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("✅ Déconnexion réussie !")
    st.info("Vous avez été déconnecté de votre compte.")
    time.sleep(2)
    st.rerun()

# ─── PAGE PRÉDICTION ──────────────────────────────────────────────────────────
elif choice == "📊 Prédiction" and st.session_state.user_id is not None:
    # Bannière personnalisée pour la page de prédiction
    create_header_banner("Prédiction")
    st.title("🎯 PRÉDICTION DE LA PRODUCTIVITÉ CACAO")
    
    # Introduction avec un conteneur stylisé
    with st.container():
        st.markdown("""
            <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #2E86AB;">📋 Instructions</h3>
                <p style="font-size:16px; color:#333;">
                    Pour obtenir une prédiction précise de votre productivité de cacao, veuillez remplir les informations suivantes.
                    Les champs sont organisés en 4 catégories :
                    <ul>
                        <li>🌱 <strong>Agronomique</strong> - Caractéristiques de votre plantation</li>
                        <li>💰 <strong>Économique</strong> - Aspects financiers</li>
                        <li>🌍 <strong>Géographique & Climatique</strong> - Localisation et conditions</li>
                        <li>👤 <strong>Socio-démographique</strong> - Informations sur l'exploitant</li>
                    </ul>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Création de tabs pour une meilleure organisation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌱 Données Agronomiques",
        "💰 Données Économiques",
        "🌍 Données Géo-Climatiques",
        "👤 Données Socio-démographiques"
    ])

    # Tab Données Agronomiques
    with tab1:
        st.markdown("### 🌱 Caractéristiques de la plantation")
        col1, col2 = st.columns(2)
        
        with col1:
            age_verger = st.number_input(
                "Âge du verger (années)",
                min_value=0.0,
                format="%.1f",
                help="Âge moyen des cacaoyers dans la parcelle."
            )
            agroforest = st.selectbox(
                "Agroforesterie",
                ("Oui", "Non"),
                help="Présence d'arbres d'ombrage ou d'associations culturales."
            )
            engrais = st.selectbox(
                "Engrais chimique",
                ("Oui", "Non"),
                help="Usage d'engrais chimiques (NPK, etc.)."
            )
            fumier = st.selectbox(
                "Fumier / Compost",
                ("Oui", "Non"),
                help="Usage d'amendements organiques."
            )
        
        with col2:
            maladie = st.selectbox(
                "Présence de maladies",
                ("Non", "oui", "Un peu"),
                help="Présence de symptômes de maladies fongiques."
            )
            herbicide = st.selectbox(
                "Utilisation d'herbicides",
                ("Oui", "Non"),
                help="Utilisation d'herbicides pour le désherbage."
            )
            insecticide = st.selectbox(
                "Utilisation d'insecticides",
                ("Oui", "Non"),
                help="Traitement contre les ravageurs."
            )
            fongicide = st.selectbox(
                "Utilisation de fongicides",
                ("Oui", "Non"),
                help="Traitement préventif/curatif contre les champignons."
            )

    # Tab Données Économiques
    with tab2:
        st.markdown("### 💰 Données Économiques", unsafe_allow_html=True)
        eco_cols = st.columns(2)
        with eco_cols[0]:
            cout_prod = st.number_input(
                "Coût de production (FCFA/ha)",
                min_value=0.0,
                format="%.2f",
                help="Total des dépenses par hectare (intrants, main-d'œuvre, etc.)."
            )
        with eco_cols[1]:
            prix_a = st.number_input(
                "Prix d'achat (FCFA/tonne)",
                min_value=0.0,
                value=750000.0,
                format="%.2f",
                help="Prix d'achat du cacao par tonne"
            )
        st.markdown("---")

    # Tab Données Géo-Climatiques
    with tab3:
        st.markdown("### 🌍 Localisation et climat")
        col1, col2 = st.columns(2)
        
        with col1:
            region = st.selectbox(
                "Région",
                ("Indenie-Djuablin", "Yamoussoukro", "La Me", "San-Pedro", "Grand-Ponts"),
                help="Région administrative de la parcelle."
            )
            
            # Ajout d'une carte (placeholder)
            st.markdown("""
                <div style="background-color: #eef7fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p>📍 Région sélectionnée : <strong>{}</strong></p>
                </div>
            """.format(region), unsafe_allow_html=True)
            
        with col2:
            pluviometrie = st.selectbox(
                "Niveau de pluviométrie",
                ("Moyenne", "Élevée", "Faible"),
                help="Régime annuel des précipitations."
            )
            
            # Indication visuelle du niveau de pluviométrie
            pluv_colors = {"Faible": "🔴", "Moyenne": "🟡", "Élevée": "🟢"}
            st.markdown(f"""
                <div style="background-color: #eef7fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p>Niveau de pluviométrie : {pluv_colors[pluviometrie]} <strong>{pluviometrie}</strong></p>
                </div>
            """, unsafe_allow_html=True)

    # Tab Données Socio-démographiques
    with tab4:
        st.markdown("### 👤 Informations sur l'exploitant")
        col1, col2 = st.columns(2)
        
        with col1:
            sexe = st.selectbox(
                "Genre",
                ("Masculin", "Feminin"),
                help="Genre du répondant."
            )
        with col2:
            competences = st.selectbox(
                "Niveau d'alphabétisation",
                ("oui, lire et écrire", "oui, lire seulement", "non"),
                help="Capacité de lire et écrire."
            )

    # Bouton de prédiction avec style
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔮 Calculer la prédiction", use_container_width=True):
            # Création du dictionnaire de données
            data = {
                "Coût_production/ha": [cout_prod],
                "Age_verger": [age_verger],
                "Région": [region],
                "Pluviometrie": [pluviometrie],
                "Sexe": [sexe],
                "Niveau_education": ["Non renseigné"],
                "Competences": [competences],
                "Engrais chimique": [engrais],
                "Agroforesterie": [agroforest],
                "fumier/ compost": [fumier],
                "Herbicide": [herbicide],
                "Insecticide": [insecticide],
                "Fongicide": [fongicide],
                "Maladie": [maladie],
            }
            
            # Création du DataFrame et prédiction
            df_input = pd.DataFrame(data)
            X_trans = xgb_model.named_steps["prep"].transform(df_input)
            pred = xgb_model.named_steps["model"].predict(X_trans)[0]
            
            # Variables pour les calculs
            production = pred  # t/ha
            production_kg = production * 1000  # Conversion en kg/ha
            prix_vente = prix_a  # Prix en FCFA/kg
            revenu = round(production_kg * prix_vente)  # FCFA/ha
            benefice = round(revenu - cout_prod)  # FCFA/ha
            
            # Fonction pour formater les grands nombres avec espace comme séparateur
            def format_number(n):
                return f"{n:,.0f}".replace(",", " ")
            
            # Style CSS commun pour les cartes
            card_style = """
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                height: 100%;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 120px;
            """
            
            # Affichage en 3 colonnes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style="{card_style}">
                        <div style="margin-bottom: 15px;">
                            <h3 style="color: #2E86AB; font-size: 14px; margin: 0; letter-spacing: 1px;">
                                Production Estimée
                            </h3>
                        </div>
                        <div>
                            <p style="font-size: 22px; font-weight: bold; color: #2E8B57; margin: 0; line-height: 1;">
                                {production:.3f}
                                <span style="font-size: 14px; font-weight: normal; display: inline-block; margin-left: 5px;">
                                    t/ha
                                </span>
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="{card_style}">
                        <div style="margin-bottom: 15px;">
                            <h3 style="color: #2E86AB; font-size: 14px; margin: 0; letter-spacing: 1px;">
                                Revenu Potentiel
                            </h3>
                        </div>
                        <div>
                            <p style="font-size: 22px; font-weight: bold; color: #2E8B57; margin: 0; line-height: 1;">
                                {format_number(revenu)}
                                <span style="font-size: 14px; font-weight: normal; display: inline-block; margin-left: 5px;">
                                    FCFA/ha
                                </span>
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style="{card_style}">
                        <div style="margin-bottom: 15px;">
                            <h3 style="color: #2E86AB; font-size: 14px; margin: 0; letter-spacing: 1px;">
                                Bénéfice Estimé
                            </h3>
                        </div>
                        <div>
                            <p style="font-size: 22px; font-weight: bold; color: {('#2E8B57' if benefice >= 0 else '#d32f2f')}; margin: 0; line-height: 1;">
                                {format_number(benefice)}
                                <span style="font-size: 14px; font-weight: normal; display: inline-block; margin-left: 5px;">
                                    FCFA/ha
                                </span>
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Détails du calcul
            st.markdown(f"""
                <div style="font-size:13px; color:#666; margin-top:20px; text-align:left; padding:15px; background-color:rgba(255,255,255,0.9); border-radius:10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <p style="font-weight:bold; color:#1a472a; margin-bottom:10px;">💡 Détails des calculs :</p>
                    <ul style="list-style-type:none; padding-left:10px;">
                        <li style="margin-bottom:6px;">• Prix : {format_number(prix_vente)} FCFA/kg</li>
                        <li style="margin-bottom:6px;">• Production : {production:.3f} t/ha = {format_number(production_kg)} kg/ha</li>
                        <li style="margin-bottom:6px;">• Revenu = Production × Prix = {format_number(production_kg)} × {format_number(prix_vente)} = {format_number(revenu)} FCFA/ha</li>
                        <li style="margin-bottom:6px;">• Coût de production : {format_number(cout_prod)} FCFA/ha</li>
                        <li style="margin-bottom:6px;">• Bénéfice = Revenu − Coût = {format_number(revenu)} − {format_number(cout_prod)} = {format_number(benefice)} FCFA/ha</li>
                    </ul>
                </div>
                
                <p style="font-size:13px; color:#666; margin-top:15px; font-style:italic; text-align:center;">
                    Ces estimations sont basées sur les paramètres fournis.<br>
                    Les résultats réels peuvent varier en fonction des conditions du marché et d'autres facteurs.
                </p>
            """, unsafe_allow_html=True)

            # Nouvelle section pour l'analyse détaillée et les recommandations
            st.markdown("### 📊 Analyse détaillée et recommandations")
            st.markdown("""
                <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 15px;">
                    <h4 style="color: #2E86AB; font-size: 15px; margin-bottom: 8px;">Analyse de la productivité :</h4>
                    <p style="font-size: 13px;">Votre production estimée de {:.3f} t/ha est comparée à la moyenne régionale de {:.3f} t/ha.</p>
                    <h4 style="color: #2E86AB; font-size: 15px; margin: 10px 0;">Recommandations :</h4>
                    <ul style="font-size: 13px; margin: 0; padding-left: 20px;">
                        <li>Si la production est inférieure à la moyenne, envisagez d'optimiser l'utilisation des engrais et de vérifier l'état sanitaire des plants.</li>
                        <li>Si le coût de production est élevé, analysez la répartition des coûts et optimisez l'utilisation des intrants.</li>
                        <li>Pour améliorer le bénéfice, cherchez des circuits de vente plus avantageux et réduisez les coûts non essentiels.</li>
                    </ul>
                </div>
            """.format(pred, MOYENNES_REGIONALES[region]['production']), unsafe_allow_html=True)

            # Ajout des visualisations et comparaisons
            st.markdown("### 📊 Analyse comparative")
            
            # Comparaison avec les moyennes régionales
            moy_region = MOYENNES_REGIONALES[region]
            
            # Création du graphique de comparaison
            fig_comp = go.Figure()
            
            # Production
            fig_comp.add_trace(go.Bar(
                name='Votre exploitation',
                x=['Production (t/ha)', 'Coût (FCFA/ha/10000)'],
                y=[pred, cout_prod/10000],
                marker_color=['#2E8B57', '#1a472a']
            ))
            
            fig_comp.add_trace(go.Bar(
                name=f'Moyenne {region}',
                x=['Production (t/ha)', 'Coût (FCFA/ha/10000)'],
                y=[moy_region['production'], moy_region['cout']/10000],
                marker_color=['rgba(46, 139, 87, 0.5)', 'rgba(26, 71, 42, 0.5)']
            ))
            
            fig_comp.update_layout(
                title="📊 COMPARAISON AVEC LA MOYENNE RÉGIONALE",
                barmode='group',
                plot_bgcolor='white',
                height=400
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)

            # Graphique en anneau pour la répartition financière
            fig_fin = go.Figure(data=[go.Pie(
                labels=['Coût de production', 'Bénéfice' if benefice >= 0 else 'Perte'],
                values=[cout_prod, abs(benefice)],
                hole=.3,
                marker_colors=['#1a472a', '#2E8B57' if benefice >= 0 else '#d32f2f']
            )])
            
            fig_fin.update_layout(
                title="💰 RÉPARTITION FINANCIÈRE",
                height=400
            )
            
            st.plotly_chart(fig_fin, use_container_width=True)

            # Suggestions d'optimisation
            st.markdown("### 💡 Suggestions d'optimisation")
            
            suggestions_a_afficher = []
            if pred < moy_region['production']:
                suggestions_a_afficher.extend(SUGGESTIONS['production_faible'])
            if cout_prod > moy_region['cout']:
                suggestions_a_afficher.extend(SUGGESTIONS['cout_eleve'])
            if benefice < moy_region['production'] * prix_a - moy_region['cout']:
                suggestions_a_afficher.extend(SUGGESTIONS['benefice_faible'])

            if suggestions_a_afficher:
                st.markdown("""
                    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px;">
                        <h4 style="color: #2E86AB;">Pistes d'amélioration :</h4>
                        <ul style="list-style-type: none; padding-left: 0;">
                """, unsafe_allow_html=True)
                
                for suggestion in suggestions_a_afficher:
                    st.markdown(f"<li style='margin: 10px 0;'>{suggestion}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # Indicateurs de performance
            st.markdown("### 📈 Indicateurs de performance")
            
            # Style pour les tooltips d'aide
            help_style = """
                <style>
                    .tooltip {
                        position: relative;
                        display: inline-block;
                        cursor: help;
                        font-size: 13px;
                    }
                    .tooltip .tooltiptext {
                        visibility: hidden;
                        width: 280px;
                        background-color: #f8f9fa;
                        color: #666;
                        text-align: left;
                        border-radius: 6px;
                        padding: 8px;
                        border: 1px solid #ddd;
                        position: absolute;
                        z-index: 1;
                        bottom: 125%;
                        left: 50%;
                        margin-left: -140px;
                        opacity: 0;
                        transition: opacity 0.3s;
                        font-size: 12px;
                        line-height: 1.4;
                    }
                    .tooltip:hover .tooltiptext {
                        visibility: visible;
                        opacity: 1;
                    }
                </style>
            """
            st.markdown(help_style, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                prod_ratio = (pred / moy_region['production']) * 100
                delta_prod = prod_ratio - 100
                st.metric(
                    "Production vs Moyenne régionale",
                    f"{prod_ratio:.1f}%",
                    f"{delta_prod:.1f}%",
                    help="Compare votre production à la moyenne de votre région. Un pourcentage > 100% signifie que vous produisez plus que la moyenne."
                )
                st.markdown("""
                    <div class="tooltip">ℹ️ Comprendre cet indicateur
                        <span class="tooltiptext">
                            • Mesure votre niveau de production par rapport à la moyenne régionale<br>
                            • > 100% : Production supérieure à la moyenne<br>
                            • < 100% : Production inférieure à la moyenne<br>
                            • La variation (↑↓) montre l'écart avec la moyenne
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                cout_ratio = (cout_prod / moy_region['cout']) * 100
                delta_cout = 100 - cout_ratio  # Inversé car moins de coût est positif
                st.metric(
                    "Coût vs Moyenne régionale",
                    f"{cout_ratio:.1f}%",
                    f"{delta_cout:.1f}%",
                    help="Compare vos coûts à la moyenne régionale. Un pourcentage < 100% signifie que vos coûts sont inférieurs à la moyenne."
                )
                st.markdown("""
                    <div class="tooltip">ℹ️ Comprendre cet indicateur
                        <span class="tooltiptext">
                            • Mesure vos coûts par rapport à la moyenne régionale<br>
                            • < 100% : Coûts inférieurs à la moyenne (positif)<br>
                            • > 100% : Coûts supérieurs à la moyenne (négatif)<br>
                            • La variation (↑↓) montre l'économie ou le surcoût
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                moy_benefice = moy_region['production'] * prix_a - moy_region['cout']
                benef_ratio = (benefice / moy_benefice) * 100 if moy_benefice > 0 else 0
                delta_benef = benef_ratio - 100
                st.metric(
                    "Bénéfice vs Moyenne régionale",
                    f"{benef_ratio:.1f}%",
                    f"{delta_benef:.1f}%",
                    help="Compare votre bénéfice au bénéfice moyen de la région. Un pourcentage > 100% signifie que votre bénéfice est supérieur à la moyenne."
                )
                st.markdown("""
                    <div class="tooltip">ℹ️ Comprendre cet indicateur
                        <span class="tooltiptext">
                            • Mesure votre rentabilité par rapport à la moyenne régionale<br>
                            • > 100% : Bénéfice supérieur à la moyenne<br>
                            • < 100% : Bénéfice inférieur à la moyenne<br>
                            • La variation (↑↓) montre l'écart de performance
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            # Ajout d'une explication générale
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <p style="color: #666; margin-bottom: 10px;"><strong>📊 Comment interpréter ces indicateurs ?</strong></p>
                    <ul style="color: #666; margin-bottom: 0;">
                        <li>Ces indicateurs comparent vos performances avec les moyennes de votre région</li>
                        <li>Les pourcentages montrent votre position par rapport à la moyenne (100%)</li>
                        <li>Les variations (↑↓) indiquent si vous êtes au-dessus ou en-dessous de la moyenne</li>
                        <li>Passez votre souris sur "ℹ️ Comprendre cet indicateur" pour plus de détails</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# ─── PAGE SOUMISSION DE DONNÉES ────────────────────────────────────────────────
elif choice == "📥 Soumettre données" and st.session_state.user_id is not None:
    # Bannière personnalisée pour la page de soumission
    create_header_banner("Soumettre")
    st.title("📊 SOUMETTRE VOS DONNÉES ANNUELLES RÉELLES")
    st.markdown(
        """
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
            <h3 style="color: #2E86AB;">📋 Instructions</h3>
            <p style="font-size:16px; color:#333;">
                Pour améliorer la précision de notre modèle, merci de soumettre vos données réelles.
                Les champs sont organisés en 3 catégories :
                <ul>
                    <li>🌱 <strong>Agronomique</strong> - Caractéristiques de votre plantation</li>
                    <li>💰 <strong>Économique</strong> - Aspects financiers</li>
                    <li>🌍 <strong>Géographique & Climatique</strong> - Localisation et conditions</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Date d'ajout
    date_ajout = st.date_input(
        "Date de soumission",
        value=date.today(),
        help="Date à laquelle vous soumettez ces données.",
    )

    # Création de tabs pour une meilleure organisation
    tab1, tab2, tab3 = st.tabs([
        "🌱 Données Agronomiques",
        "💰 Données Économiques",
        "🌍 Données Géo-Climatiques"
    ])

    # Tab Données Agronomiques
    with tab1:
        st.markdown("### 🌱 Caractéristiques de la plantation")
        col1, col2 = st.columns(2)
        
        with col1:
            age_verger2 = st.number_input(
                "Âge du verger (années)",
                min_value=0.0,
                format="%.1f",
                key="s_age",
                help="Âge moyen des cacaoyers dans la parcelle"
            )
            agroforest2 = st.selectbox(
                "Agroforesterie",
                ("Oui", "Non"),
                key="s_agro",
                help="Présence d'arbres d'ombrage ou d'associations culturales"
            )
            engrais2 = st.selectbox(
                "Utilisation d'engrais",
                ("Oui", "Non"),
                key="s_engrais",
                help="Usage d'engrais chimiques (NPK, etc.)"
            )
            fumier2 = st.selectbox(
                "Utilisation de fumier/compost",
                ("Oui", "Non"),
                key="s_fumier",
                help="Usage d'amendements organiques"
            )
        
        with col2:
            maladie2 = st.selectbox(
                "Présence de maladies",
                ("Non", "Un peu", "Oui"),
                key="s_maladie",
                help="Présence de symptômes de maladies"
            )
            herbicide2 = st.selectbox(
                "Utilisation d'herbicides",
                ("Oui", "Non"),
                key="s_herb",
                help="Utilisation de produits pour le désherbage"
            )
            insecticide2 = st.selectbox(
                "Utilisation d'insecticides",
                ("Oui", "Non"),
                key="s_insect",
                help="Traitement contre les insectes ravageurs"
            )
            fongicide2 = st.selectbox(
                "Utilisation de fongicides",
                ("Oui", "Non"),
                key="s_fongi",
                help="Traitement contre les maladies fongiques"
            )

    # Tab Données Économiques
    with tab2:
        st.markdown("### 💰 Données Économiques")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cout_prod = st.number_input(
                "Coût de production (FCFA/ha)",
                min_value=0.0,
                step=10000.0,
                format="%.0f",
                key="s_cout",
                help="Total des dépenses par hectare (intrants, main-d'œuvre, etc.)"
            )
        with col2:
            prix_a = st.number_input(
                "Prix d'achat (FCFA/kg)",
                min_value=0.0,
                value=750.0,
                step=50.0,
                format="%.0f",
                key="s_prix",
                help="Prix d'achat du cacao par kilogramme"
            )
        with col3:
            product2 = st.number_input(
                "Productivité réelle (t/ha)",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.3f",
                key="s_prod",
                help="Production réelle obtenue en tonnes par hectare"
            )

    # Tab Données Géo-Climatiques
    with tab3:
        st.markdown("### 🌍 Localisation et climat")
        col1, col2 = st.columns(2)
        
        with col1:
            region2 = st.selectbox(
                "Région",
                ("Indenie-Djuablin", "Yamoussoukro", "La Me", "San-Pedro", "Grand-Ponts"),
                key="s_region",
                help="Région administrative de la parcelle"
            )
            
            # Affichage de la région sélectionnée
            st.markdown(f"""
                <div style="background-color: #eef7fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p>📍 Région sélectionnée : <strong>{region2}</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            pluviometrie2 = st.selectbox(
                "Niveau de pluviométrie",
                ("Moyenne", "Élevée", "Faible"),
                key="s_pluv",
                help="Régime des précipitations de l'année"
            )
            
            # Indication visuelle du niveau de pluviométrie
            pluv_colors = {"Faible": "🔴", "Moyenne": "🟡", "Élevée": "🟢"}
            st.markdown(f"""
                <div style="background-color: #eef7fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p>Niveau de pluviométrie : {pluv_colors[pluviometrie2]} <strong>{pluviometrie2}</strong></p>
                </div>
            """, unsafe_allow_html=True)

    # Bouton de soumission
    st.markdown("---")
    if st.button("💾 Enregistrer mes données", use_container_width=True):
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO submissions (
                user_id,
                Cout_production,
                Age_verger,
                Region,
                Niveau_education,
                Competences,
                Engrais,
                Agroforesterie,
                Fumier,
                Herbicide,
                Insecticide,
                Fongicide,
                Pluviometrie,
                Maladie,
                Sexe,
                Productivite,
                submitted_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                st.session_state.user_id,
                cout_prod,
                age_verger2,
                region2,
                "Non renseigné",  # Niveau_education par défaut
                "Non renseigné",  # Competences par défaut
                engrais2,
                agroforest2,
                fumier2,
                herbicide2,
                insecticide2,
                fongicide2,
                pluviometrie2,
                maladie2,
                "Non renseigné",  # Sexe par défaut
                product2,
                date_ajout.isoformat(),
            ),
        )
        conn.commit()
        conn.close()
        
        st.success("✅ Données enregistrées avec succès ! Merci pour votre contribution.")
        st.balloons()  # Petit effet de célébration

# ─── PAGE "MES DONNÉES" ────────────────────────────────────────────────────────
elif choice == "📂 Mes données" and st.session_state.user_id is not None:
    # Bannière personnalisée pour la page historique
    create_header_banner("Historique")
    st.title("📈 HISTORIQUE DE MES DONNÉES")
    
    # Introduction stylisée
    st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
            <h3 style="color: #2E86AB;">📊 Vue d'ensemble de vos données</h3>
            <p style="font-size:16px; color:#333;">
                Consultez l'historique de vos soumissions et analysez l'évolution de vos performances.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Récupération des données
    conn = get_db_connection()
    query = """
        SELECT
            id AS submission_id,
            Cout_production AS Cout_production_ha,
            Age_verger,
            Region,
            Engrais,
            Agroforesterie,
            Fumier,
            Herbicide,
            Insecticide,
            Fongicide,
            Pluviometrie,
            Maladie,
            Productivite,
            submitted_at AS date_ajout
        FROM submissions
        WHERE user_id = ?
        ORDER BY submitted_at DESC
    """
    df_user = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
    conn.close()

    if df_user.empty:
        st.info("📝 Vous n'avez encore soumis aucune donnée. Commencez par soumettre vos premières données dans l'onglet 'Soumettre données'.")
    else:
        # Onglets pour différentes vues
        tab1, tab2, tab3 = st.tabs(["📊 Tableau de données", "📈 Analyses", "📥 Exporter"])

        # Onglet Tableau de données
        with tab1:
            st.markdown("### 📋 Vos données soumises")
            
            # Formatage des colonnes pour un meilleur affichage
            df_display = df_user.copy()
            df_display['date_ajout'] = pd.to_datetime(df_display['date_ajout']).dt.strftime('%d/%m/%Y')
            df_display['Cout_production_ha'] = df_display['Cout_production_ha'].apply(lambda x: f"{x:,.0f} FCFA".replace(",", " "))
            df_display['Productivite'] = df_display['Productivite'].apply(lambda x: f"{x:.3f} t/ha")
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )

        # Onglet Analyses
        with tab2:
            st.markdown("### 📊 Analyse de vos données")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la productivité
                fig_prod = px.line(
                    df_user,
                    x='date_ajout',
                    y='Productivite',
                    title='📈 ÉVOLUTION DE VOTRE PRODUCTIVITÉ',
                    labels={'date_ajout': 'Date', 'Productivite': 'Productivité (t/ha)'}
                )
                fig_prod.update_layout(
                    plot_bgcolor='white',
                    showlegend=False
                )
                st.plotly_chart(fig_prod, use_container_width=True)

            with col2:
                # Évolution des coûts
                fig_cout = px.line(
                    df_user,
                    x='date_ajout',
                    y='Cout_production_ha',
                    title='💸 ÉVOLUTION DE VOS COÛTS DE PRODUCTION',
                    labels={'date_ajout': 'Date', 'Cout_production_ha': 'Coût (FCFA/ha)'}
                )
                fig_cout.update_layout(
                    plot_bgcolor='white',
                    showlegend=False
                )
                st.plotly_chart(fig_cout, use_container_width=True)

            # Statistiques descriptives
            st.markdown("### 📈 Statistiques clés")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                prod_moy = df_user['Productivite'].mean()
                prod_max = df_user['Productivite'].max()
                st.metric(
                    "Productivité moyenne",
                    f"{prod_moy:.3f} t/ha",
                    f"{((prod_max - prod_moy)/prod_moy)*100:.1f}% (max)",
                    help="Votre productivité moyenne et l'écart avec votre meilleur résultat"
                )

            with col2:
                cout_moy = df_user['Cout_production_ha'].mean()
                cout_min = df_user['Cout_production_ha'].min()
                st.metric(
                    "Coût moyen",
                    f"{cout_moy:,.0f} FCFA/ha".replace(",", " "),
                    f"{((cout_min - cout_moy)/cout_moy)*100:.1f}% (min)",
                    help="Votre coût moyen et l'écart avec votre coût minimum"
                )

            with col3:
                nb_submissions = len(df_user)
                st.metric(
                    "Nombre de soumissions",
                    nb_submissions,
                    help="Nombre total de données que vous avez soumises"
                )

            # Analyse des pratiques agricoles
            st.markdown("### 🌱 Analyse des pratiques")
            col1, col2 = st.columns(2)
            
            with col1:
                pratiques = pd.DataFrame({
                    'Pratique': ['Engrais', 'Agroforesterie', 'Fumier', 'Herbicide', 'Insecticide', 'Fongicide'],
                    'Utilisation': [
                        (df_user['Engrais'] == 'Oui').mean() * 100,
                        (df_user['Agroforesterie'] == 'Oui').mean() * 100,
                        (df_user['Fumier'] == 'Oui').mean() * 100,
                        (df_user['Herbicide'] == 'Oui').mean() * 100,
                        (df_user['Insecticide'] == 'Oui').mean() * 100,
                        (df_user['Fongicide'] == 'Oui').mean() * 100
                    ]
                })
                
                fig_pratiques = px.bar(
                    pratiques,
                    x='Pratique',
                    y='Utilisation',
                    title='🌱 TAUX D\'UTILISATION DES PRATIQUES AGRICOLES (%)',
                    labels={'Utilisation': '%'}
                )
                fig_pratiques.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig_pratiques, use_container_width=True)

            with col2:
                # Distribution des régions
                region_counts = df_user['Region'].value_counts()
                fig_regions = px.pie(
                    values=region_counts.values,
                    names=region_counts.index,
                    title='🗺️ RÉPARTITION PAR RÉGION'
                )
                st.plotly_chart(fig_regions, use_container_width=True)

        # Onglet Export
        with tab3:
            st.markdown("### 📥 Exporter vos données")
            
            # Export CSV
            csv = df_user.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger au format CSV",
                data=csv,
                file_name="mes_donnees_cacao.csv",
                mime="text/csv",
                help="Téléchargez vos données au format CSV pour les analyser dans un tableur"
            )
            
            # Aperçu des données à exporter
            with st.expander("👁️ Aperçu des données à exporter"):
                st.dataframe(df_user.head(), use_container_width=True)

# ─── PAGE "ASSISTANT IA" ──────────────────────────────────────────────────────
elif choice == "🤖 Assistant IA" and st.session_state.user_id is not None:
    # Bannière personnalisée pour l'assistant IA
    create_header_banner("Assistant")
    st.title("🤖 ASSISTANT IA")
    
    st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
            <h3 style="color: #2E86AB;">🤖 Assistant IA Mon Cacao</h3>
            <p style="font-size:16px; color:#333;">
                Votre assistant personnel pour optimiser votre production de cacao :
                <ul>
                    <li>💬 Questions-réponses en temps réel</li>
                    <li>📊 Analyse de vos données</li>
                    <li>🌱 Conseils personnalisés</li>
                    <li>📈 Prédictions avancées</li>
                </ul>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Interface de chat avec l'IA
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Interface de saisie
    if prompt := st.chat_input("Posez votre question à l'assistant IA..."):
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simuler une réponse de l'IA
        with st.chat_message("assistant"):
            response = f"🤖 **Assistant IA Mon Cacao**\n\nMerci pour votre question ! Je suis là pour vous aider avec votre production de cacao. Voici une réponse personnalisée basée sur vos données..."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ─── PAGE "CONSEILS" ──────────────────────────────────────────────────────────
elif choice == "💡 Conseils" and st.session_state.user_id is not None:
    # Bannière personnalisée pour les conseils
    create_header_banner("Conseil")
    st.title("💡 CONSEILS PERSONNALISÉS")
    
    st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
            <h3 style="color: #2E86AB;">💡 Conseils pour optimiser votre production</h3>
            <p style="font-size:16px; color:#333;">
                Découvrez des conseils personnalisés basés sur vos données et les meilleures pratiques :
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Conseils par catégorie
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌱 Pratiques agricoles")
        st.info("""
        **Fertilisation optimale :**
        - Utilisez des engrais organiques
        - Respectez les doses recommandées
        - Fertilisez en début de saison des pluies
        """)
        
        st.markdown("### 💧 Gestion de l'eau")
        st.success("""
        **Irrigation efficace :**
        - Maintenez une humidité constante
        - Évitez l'excès d'eau
        - Utilisez le paillage
        """)
    
    with col2:
        st.markdown("### 🛡️ Protection des cultures")
        st.warning("""
        **Lutte contre les maladies :**
        - Surveillez régulièrement vos plants
        - Traitez préventivement
        - Utilisez des variétés résistantes
        """)
        
        st.markdown("### 📊 Optimisation des coûts")
        st.info("""
        **Réduction des coûts :**
        - Planifiez vos achats
        - Négociez avec les fournisseurs
        - Optimisez l'utilisation des intrants
        """)

# ─── PAGE "ADMIN" (OPTIONNEL) ─────────────────────────────────────────────────
elif choice == "🔒 Admin" and st.session_state.user_id is not None:
    # Bannière personnalisée pour l'espace admin
    create_header_banner("Admin")
    st.title("⚙️ ESPACE ADMIN")
    conn = get_db_connection()

    st.markdown("#### 👥 Utilisateurs enregistrés")
    df_users = pd.read_sql_query("SELECT id AS user_id, username FROM users", conn)
    st.dataframe(df_users, use_container_width=True)

    st.markdown("---")

    st.markdown("#### 🗂️ Toutes les soumissions")
    df_submissions = pd.read_sql_query(
        """
        SELECT
            s.id AS submission_id,
            u.username,
            s.Cout_production AS Cout_production_ha,
            s.Age_verger,
            s.Region,
            s.Niveau_education,
            s.Competences,
            s.Engrais,
            s.Agroforesterie,
            s.Fumier,
            s.Herbicide,
            s.Insecticide,
            s.Fongicide,
            s.Pluviometrie,
            s.Maladie,
            s.Sexe,
            s.Productivite,
            s.submitted_at AS date_ajout
        FROM submissions s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.submitted_at DESC
        """,
        conn,
    )
    conn.close()

    st.dataframe(df_submissions, use_container_width=True)
    csv_all = df_submissions.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger toutes les soumissions (CSV)",
        data=csv_all,
        file_name="toutes_soumissions_cacao.csv",
        mime="text/csv",
    )

# ─── CAS PAR DÉFAUT (non connecté) ──────────────────────────────────────────────
else:
    st.write("Veuillez vous connecter pour accéder à cette section.")
