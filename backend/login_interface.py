import streamlit as st
from auth_system import auth
import pandas as pd

def show_login_page():
    """Affiche la page de connexion/inscription"""
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #2E8B57 0%, #1a472a 100%); 
                    color: white; padding: 3rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">🌱 MON CACAO</h1>
            <h2 style="font-size: 1.5rem; margin-bottom: 1rem;">IA PRÉDICTIVE & ANALYSE ÉCOLOGIQUE</h2>
            <p style="font-size: 1.1rem;">Connectez-vous ou créez votre compte pour accéder à l'application</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Onglets pour connexion/inscription
    tab1, tab2 = st.tabs(["🔐 Connexion", "📝 Inscription"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()

def show_login_form():
    """Formulaire de connexion"""
    st.markdown("### 🔐 Connexion à votre compte")
    
    with st.form("login_form"):
        email = st.text_input("📧 Adresse e-mail", placeholder="votre@email.com")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Votre mot de passe")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_login = st.form_submit_button("🚀 Se connecter", use_container_width=True)
        with col2:
            forgot_password = st.form_submit_button("❓ Mot de passe oublié", use_container_width=True)
        
        if submit_login:
            if email and password:
                success, result = auth.login_user(email, password)
                if success:
                    st.session_state.user_id = result["user_id"]
                    st.session_state.username = result["username"]
                    st.session_state.session_token = result["session_token"]
                    st.session_state.logged_in = True
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs")
        
        if forgot_password:
            st.info("📧 Fonctionnalité de récupération de mot de passe en cours de développement")

def show_register_form():
    """Formulaire d'inscription"""
    st.markdown("### 📝 Créer un nouveau compte")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("👤 Nom d'utilisateur", placeholder="votre_username")
            email = st.text_input("📧 Adresse e-mail", placeholder="votre@email.com")
            password = st.text_input("🔒 Mot de passe", type="password", placeholder="8+ caractères")
            confirm_password = st.text_input("🔒 Confirmer le mot de passe", type="password")
        
        with col2:
            first_name = st.text_input("📝 Prénom", placeholder="Votre prénom")
            last_name = st.text_input("📝 Nom de famille", placeholder="Votre nom")
            region = st.selectbox("🌍 Région de production", [
                "Abidjan", "San-Pédro", "Gagnoa", "Divo", "Yamoussoukro",
                "Bouaké", "Korhogo", "Man", "Daloa", "Autre"
            ])
            user_type = st.selectbox("👨‍🌾 Type d'utilisateur", [
                "agriculteur", "coopérative", "technicien", "chercheur", "autre"
            ])
        
        # Politique de confidentialité
        st.markdown("---")
        st.markdown("### 📋 Politique de confidentialité")
        
        with open("POLITIQUE_GESTION_DONNEES.md", "r", encoding="utf-8") as f:
            policy_content = f.read()
        
        with st.expander("📖 Lire la politique de gestion des données"):
            st.markdown(policy_content)
        
        consent_gdpr = st.checkbox(
            "✅ J'accepte la politique de gestion des données et j'autorise le traitement de mes données personnelles",
            value=False
        )
        
        submit_register = st.form_submit_button("🚀 Créer mon compte", use_container_width=True)
        
        if submit_register:
            if not all([username, email, password, confirm_password]):
                st.warning("⚠️ Veuillez remplir tous les champs obligatoires")
            elif password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas")
            elif not consent_gdpr:
                st.error("❌ Vous devez accepter la politique de gestion des données")
            else:
                success, result = auth.register_user(
                    username, email, password, first_name, last_name, region, user_type
                )
                if success:
                    st.success(f"✅ {result}")
                    st.info("🔄 Vous pouvez maintenant vous connecter avec vos identifiants")
                else:
                    st.error(f"❌ {result}")

def show_user_dashboard():
    """Tableau de bord utilisateur après connexion"""
    if not st.session_state.get("logged_in"):
        return False
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                    color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h2 style="margin: 0;">🎉 Bienvenue, {st.session_state.username} !</h2>
            <p style="margin: 0.5rem 0 0 0;">Vous êtes maintenant connecté à MON CACAO</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Statistiques utilisateur
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Utilisateur", st.session_state.username)
    
    with col2:
        st.metric("🆔 ID", st.session_state.user_id)
    
    with col3:
        st.metric("🔐 Statut", "Connecté")
    
    # Bouton de déconnexion
    if st.button("🚪 Se déconnecter", type="primary"):
        auth.logout_user(st.session_state.session_token)
        for key in ["user_id", "username", "session_token", "logged_in"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ Déconnexion réussie")
        st.rerun()
    
    return True

def check_authentication():
    """Vérifie l'authentification de l'utilisateur"""
    if "session_token" in st.session_state:
        success, result = auth.verify_session(st.session_state.session_token)
        if success:
            st.session_state.user_id = result["user_id"]
            st.session_state.username = result["username"]
            return True
        else:
            # Session expirée
            for key in ["user_id", "username", "session_token", "logged_in"]:
                if key in st.session_state:
                    del st.session_state[key]
    
    return False

def main():
    """Fonction principale de l'interface d'authentification"""
    st.set_page_config(
        page_title="🔐 Connexion - MON CACAO",
        page_icon="🌱",
        layout="wide"
    )
    
    # Vérification de l'authentification
    if check_authentication():
        if show_user_dashboard():
            st.success("✅ Authentification réussie ! Redirection vers l'application principale...")
            # Ici, vous pouvez rediriger vers l'application principale
            return True
    else:
        show_login_page()
    
    return False

if __name__ == "__main__":
    main()
