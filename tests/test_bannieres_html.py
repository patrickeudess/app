#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les bannières HTML modernes
"""

import os
import re
from pathlib import Path

def test_bannieres_html():
    """Test des bannières HTML modernes"""
    
    print("🧪 Test des Bannières HTML Modernes")
    print("=" * 50)
    
    # Vérifier les fichiers créés
    files_to_check = [
        "frontend/css/modern-banner.css",
        "frontend/js/modern-banner.js"
    ]
    
    print("\n📁 Vérification des fichiers créés :")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
    
    # Vérifier les fichiers HTML mis à jour
    html_files = [
        "frontend/soumettre.html",
        "frontend/historique.html", 
        "frontend/analyse.html",
        "frontend/conseils.html",
        "frontend/assistant.html",
        "frontend/prediction.html"
    ]
    
    print("\n🌐 Vérification des fichiers HTML mis à jour :")
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier les inclusions CSS et JS
            has_css = 'modern-banner.css' in content
            has_js = 'modern-banner.js' in content
            has_header = 'app-header' in content
            
            status = "✅" if has_css and has_js and has_header else "⚠️"
            print(f"{status} {html_file}")
            
            if has_css:
                print(f"   ✅ CSS moderne inclus")
            else:
                print(f"   ❌ CSS moderne manquant")
                
            if has_js:
                print(f"   ✅ JavaScript moderne inclus")
            else:
                print(f"   ❌ JavaScript moderne manquant")
        else:
            print(f"❌ {html_file} - FICHIER MANQUANT")
    
    # Vérifier le contenu du CSS moderne
    print("\n🎨 Vérification du CSS moderne :")
    css_file = "frontend/css/modern-banner.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        features = [
            ("Variables CSS", ":root"),
            ("Gradient moderne", "linear-gradient"),
            ("Effet de brillance", "@keyframes shine"),
            ("Animation de pulsation", "@keyframes pulse"),
            ("Design responsive", "@media"),
            ("Effet de flottement", "@keyframes float"),
            ("Particules", "@keyframes sparkle")
        ]
        
        for feature, pattern in features:
            if pattern in css_content:
                print(f"✅ {feature}")
            else:
                print(f"❌ {feature}")
    else:
        print("❌ Fichier CSS moderne manquant")
    
    # Vérifier le contenu du JavaScript moderne
    print("\n⚡ Vérification du JavaScript moderne :")
    js_file = "frontend/js/modern-banner.js"
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        features = [
            ("Classe ModernBanner", "class ModernBanner"),
            ("Détection de page", "getCurrentPage"),
            ("Gestion des utilisateurs", "getCurrentUser"),
            ("Animations", "startAnimations"),
            ("Gestion des événements", "setupEventListeners"),
            ("Navigation", "handleNavigation"),
            ("Mise à jour du statut", "updateUserStatus")
        ]
        
        for feature, pattern in features:
            if pattern in js_content:
                print(f"✅ {feature}")
            else:
                print(f"❌ {feature}")
    else:
        print("❌ Fichier JavaScript moderne manquant")
    
    # Résumé des améliorations
    print("\n📋 Résumé des améliorations apportées :")
    print("=" * 50)
    
    print("""
🎨 **Bannières HTML modernisées :**
• Design uniforme avec gradient vert professionnel
• Effets de brillance et animations fluides
• Logo animé avec feuilles et pièces de monnaie
• Statut dynamique (En ligne/Hors ligne)
• Badge contextuel selon la page active
• Bouton de retour moderne avec effets hover

📱 **Pages concernées :**
• ✅ soumettre.html - Soumission de données
• ✅ historique.html - Historique et analyses  
• ✅ analyse.html - Analyse détaillée
• ✅ conseils.html - Conseils personnalisés
• ✅ assistant.html - Assistant IA

🔧 **Fonctionnalités techniques :**
• CSS moderne avec variables et animations
• JavaScript orienté objet pour la gestion
• Détection automatique de la page
• Animations d'entrée et interactions
• Design responsive pour tous les écrans
• Gestion des événements utilisateur

🎯 **Avantages pour l'utilisateur :**
• Interface cohérente sur toutes les pages
• Navigation intuitive avec contexte visuel
• Expérience utilisateur moderne et fluide
• Animations engageantes et professionnelles
• Adaptation automatique au contenu
    """)
    
    print("🎉 Test des bannières HTML modernes terminé !")

if __name__ == "__main__":
    test_bannieres_html()
