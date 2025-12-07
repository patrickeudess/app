#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la page Score Écologique
"""

import os
import re

def test_score_ecologique():
    """Test de la page Score Écologique"""
    
    print("🌍 Test de la Page Score Écologique")
    print("=" * 50)
    
    # Vérifier les fichiers
    files_to_check = [
        "frontend/score-ecologique.html",
        "frontend/index.html"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - FICHIER TROUVÉ")
        else:
            print(f"❌ {file_path} - FICHIER MANQUANT")
    
    # Vérifier la navigation dans index.html
    index_file = "frontend/index.html"
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n🧭 Vérification de la navigation :")
        
        nav_features = [
            ("Carte Score Écologique", "Score Écologique"),
            ("Lien vers la page", "score-ecologique.html"),
            ("Icône écologique", "fas fa-leaf"),
            ("Badge Nouveau", "feature-badge")
        ]
        
        for feature_name, pattern in nav_features:
            if pattern in content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
    
    # Vérifier le style CSS
    css_file = "frontend/css/style.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        print("\n🎨 Vérification des styles CSS :")
        
        css_features = [
            ("Style eco-icon", ".eco-icon"),
            ("Gradient vert", "linear-gradient(135deg, #4ade80 0%, #22c55e 100%)")
        ]
        
        for feature_name, pattern in css_features:
            if pattern in css_content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
    
    # Vérifier la page Score Écologique
    score_file = "frontend/score-ecologique.html"
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            score_content = f.read()
        
        print("\n📋 Vérification de la page Score Écologique :")
        
        page_features = [
            ("Titre de la page", "Score Écologique"),
            ("Formulaire d'évaluation", "eco-form"),
            ("Indicateurs environnementaux", "Indicateurs Environnementaux"),
            ("Fonction de calcul", "calcEcoScore()"),
            ("Historique", "Historique des Scores"),
            ("LocalStorage", "localStorage")
        ]
        
        for feature_name, pattern in page_features:
            if pattern in score_content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
        
        # Vérifier les indicateurs spécifiques
        print("\n🌱 Vérification des indicateurs :")
        
        indicators = [
            ("Arbres d'ombrage", "🌳 Arbres d'ombrage"),
            ("Couverture du sol", "🌱 Couverture du sol"),
            ("Fertilisation", "🧪 Fertilisation"),
            ("Pesticides", "🛡️ Pesticides"),
            ("Taille sanitaire", "✂️ Taille sanitaire"),
            ("Protection berges", "💧 Protection berges"),
            ("Gestion déchets", "♻️ Gestion déchets"),
            ("Biodiversité", "🐦 Biodiversité"),
            ("Déforestation", "🚫 Déforestation"),
            ("Certification", "✅ Certification")
        ]
        
        for indicator_name, pattern in indicators:
            if pattern in score_content:
                print(f"✅ {indicator_name}")
            else:
                print(f"❌ {indicator_name}")
        
        # Vérifier les fonctionnalités JavaScript
        print("\n⚡ Vérification des fonctionnalités JavaScript :")
        
        js_features = [
            ("Calcul de score", "calcEcoScore"),
            ("Affichage du résultat", "displayScore"),
            ("Sauvegarde historique", "saveToHistory"),
            ("Chargement historique", "loadHistory"),
            ("Sliders interactifs", "slider"),
            ("Boutons toggle", "toggle-btn")
        ]
        
        for feature_name, pattern in js_features:
            if pattern in score_content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
        
        # Vérifier les styles CSS inline
        print("\n🎨 Vérification des styles CSS inline :")
        
        css_inline_features = [
            ("Container principal", "eco-score-container"),
            ("Cartes d'indicateurs", "indicator-card"),
            ("Badge de score", "score-badge"),
            ("Historique", "history-section"),
            ("Responsive design", "@media")
        ]
        
        for feature_name, pattern in css_inline_features:
            if pattern in score_content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
    
    # Résumé des fonctionnalités
    print("\n📋 Résumé des fonctionnalités du Score Écologique :")
    print("=" * 50)
    
    print("""
🌍 **Page Score Écologique - Fonctionnalités :**

**📊 Indicateurs Environnementaux (10) :**
• 🌳 Arbres d'ombrage (0-3)
• 🌱 Couverture du sol (0-2)
• 🧪 Fertilisation (0-3)
• 🛡️ Pesticides (0-3)
• ✂️ Taille sanitaire (0-3)
• 💧 Protection berges (0/1)
• ♻️ Gestion déchets (0/1)
• 🐦 Biodiversité (0-2)
• 🚫 Déforestation (0/1)
• ✅ Certification (0/1)

**🧮 Calcul du Score :**
• Formule pondérée par indicateur
• Score final de 0 à 100
• 4 niveaux : Rouge (<40), Orange (40-69), Vert (70-84), Or (≥85)

**💾 Stockage et Historique :**
• Sauvegarde en localStorage
• Historique des 10 derniers scores
• Date et heure de chaque évaluation

**🎨 Interface Utilisateur :**
• Design moderne avec gradients
• Sliders interactifs pour les niveaux
• Boutons toggle pour les indicateurs binaires
• Badge coloré pour le score final
• Responsive design mobile

**📈 Recommandations :**
• Suggestions personnalisées selon le score
• Actions prioritaires d'amélioration
• Conseils pratiques pour chaque indicateur

**🔗 Intégration :**
• Navigation depuis la page d'accueil
• Icône écologique distinctive
• Badge "Nouveau" pour la visibilité
• Retour facile vers l'accueil
    """)
    
    print("🎉 Test de la page Score Écologique terminé !")

if __name__ == "__main__":
    test_score_ecologique()
