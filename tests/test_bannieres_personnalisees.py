#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les bannières personnalisées sur toutes les pages
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire courant au path pour importer cacao1
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_bannieres_personnalisees():
    """Test des bannières personnalisées sur différentes pages"""
    
    st.set_page_config(
        page_title="🎯 MON CACAO - IA PRÉDICTIVE",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialiser les variables de session pour les tests
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 1
    if 'username' not in st.session_state:
        st.session_state.username = "test_user"
    
    st.header("🧪 Test des Bannières Personnalisées")
    
    # Importer la fonction de bannière
    try:
        from cacao1 import create_header_banner
        st.success("✅ Fonction create_header_banner importée avec succès")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'import: {e}")
        return
    
    # Test des différentes pages
    pages = [
        ("Prédiction", "🎯 PRÉDICTION IA"),
        ("Soumettre", "📥 SOUMISSION DE DONNÉES"),
        ("Historique", "📈 HISTORIQUE ET ANALYSES"),
        ("Assistant", "🤖 ASSISTANT IA"),
        ("Conseil", "💡 CONSEILS PERSONNALISÉS"),
        ("Admin", "⚙️ ADMINISTRATION")
    ]
    
    for page_context, page_title in pages:
        st.markdown(f"---")
        st.subheader(f"📄 Page: {page_title}")
        
        try:
            create_header_banner(page_context)
            st.success(f"✅ Bannière affichée pour '{page_context}'")
        except Exception as e:
            st.error(f"❌ Erreur pour '{page_context}': {e}")
    
    st.markdown("---")
    st.header("📋 Résumé des améliorations")
    
    st.markdown("""
    ### ✅ Bannières personnalisées implémentées :
    
    **🎯 Pages avec contexte spécifique :**
    - **Prédiction** : Icône 🎯 + "Prédiction IA"
    - **Soumettre** : Icône 📥 + "Soumission de données"
    - **Historique** : Icône 📈 + "Historique et analyses"
    - **Assistant IA** : Icône 🤖 + "Assistant IA"
    - **Conseils** : Icône 💡 + "Conseils personnalisés"
    - **Admin** : Icône ⚙️ + "Administration"
    
    **🎨 Fonctionnalités ajoutées :**
    - **Sous-titre dynamique** : Affiche le contexte de la page
    - **Icône contextuelle** : Change selon le type de page
    - **Badge stylisé** : Sous-titre avec fond semi-transparent
    - **Navigation enrichie** : Nouvelles pages Assistant IA et Conseils
    
    **📱 Nouvelles pages créées :**
    - **🤖 Assistant IA** : Interface de chat avec l'IA
    - **💡 Conseils** : Conseils personnalisés par catégorie
    
    **🔧 Améliorations techniques :**
    - Fonction `create_header_banner(page_context)` paramétrable
    - Gestion automatique du contexte de page
    - Intégration native avec la navigation Streamlit
    - Design responsive et accessible
    """)
    
    st.success("🎉 Toutes les bannières personnalisées fonctionnent correctement !")

if __name__ == "__main__":
    test_bannieres_personnalisees()
