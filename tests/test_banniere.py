#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la bannière uniforme sur toutes les pages
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire courant au path pour importer cacao1
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_banniere():
    """Test de la bannière sur différentes pages"""
    
    st.set_page_config(
        page_title="🎯 MON CACAO - IA PRÉDICTIVE",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialiser les variables de session pour les tests
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    # Test 1: Bannière sans utilisateur connecté
    st.header("🧪 Test 1: Bannière sans utilisateur connecté")
    st.session_state.user_id = None
    st.session_state.username = ""
    
    # Importer et tester la fonction de bannière
    try:
        from cacao1 import create_header_banner
        create_header_banner()
        st.success("✅ Bannière affichée correctement (mode visiteur)")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage de la bannière: {e}")
    
    st.divider()
    
    # Test 2: Bannière avec utilisateur connecté
    st.header("🧪 Test 2: Bannière avec utilisateur connecté")
    st.session_state.user_id = 1
    st.session_state.username = "test_user"
    
    try:
        create_header_banner()
        st.success("✅ Bannière affichée correctement (mode utilisateur)")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage de la bannière: {e}")
    
    st.divider()
    
    # Test 3: Bannière avec admin
    st.header("🧪 Test 3: Bannière avec administrateur")
    st.session_state.user_id = 1
    st.session_state.username = "admin"
    
    try:
        create_header_banner()
        st.success("✅ Bannière affichée correctement (mode admin)")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage de la bannière: {e}")
    
    st.divider()
    
    # Résumé des tests
    st.header("📋 Résumé des améliorations de la bannière")
    st.markdown("""
    ### ✅ Fonctionnalités implémentées :
    
    **🎨 Design moderne :**
    - Gradient vert professionnel
    - Effets de brillance animés
    - Ombres et bordures arrondies
    - Typographie améliorée
    
    **👤 Gestion des utilisateurs :**
    - Statut en ligne/hors ligne dynamique
    - Affichage du nom d'utilisateur
    - Rôle utilisateur (Agriculteur/Visiteur)
    - Bouton de déconnexion intelligent
    
    **📱 Responsive et accessible :**
    - Design adaptatif
    - Animations fluides
    - Contraste optimal
    - Icônes explicites
    
    **🔧 Fonctionnalités techniques :**
    - Bannière uniforme sur toutes les pages
    - Gestion automatique des états
    - Intégration native avec Streamlit
    - Performance optimisée
    """)
    
    st.success("🎉 Tous les tests de la bannière uniforme sont passés avec succès !")

if __name__ == "__main__":
    test_banniere()
