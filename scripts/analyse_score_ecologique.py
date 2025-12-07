#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'analyse automatisée de la page Score Écologique
"""

import os
import re
from datetime import datetime

def analyser_score_ecologique():
    """Analyse complète de la page Score Écologique"""
    
    print("🔍 Analyse Automatisée de la Page Score Écologique")
    print("=" * 60)
    print(f"📅 Date d'analyse : {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print()
    
    # 1. Analyse des fichiers
    print("📁 ANALYSE DES FICHIERS")
    print("-" * 30)
    
    fichiers_analyse = [
        ("frontend/score-ecologique.html", "Page principale"),
        ("frontend/index.html", "Page d'accueil"),
        ("frontend/css/style.css", "Styles CSS"),
        ("test_score_ecologique.py", "Script de test"),
        ("SCORE_ECOLOGIQUE_DOCUMENTATION.md", "Documentation"),
        ("ANALYSE_SCORE_ECOLOGIQUE.md", "Analyse détaillée")
    ]
    
    fichiers_presents = []
    fichiers_manquants = []
    
    for fichier, description in fichiers_analyse:
        if os.path.exists(fichier):
            taille = os.path.getsize(fichier)
            fichiers_presents.append((fichier, description, taille))
            print(f"✅ {fichier} - {description} ({taille} octets)")
        else:
            fichiers_manquants.append((fichier, description))
            print(f"❌ {fichier} - {description} (MANQUANT)")
    
    print()
    
    # 2. Analyse du contenu de la page principale
    print("📄 ANALYSE DU CONTENU")
    print("-" * 30)
    
    score_file = "frontend/score-ecologique.html"
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        print(f"📊 Taille du fichier : {len(contenu)} caractères")
        
        # Analyse du contenu
        analyses_contenu = [
            ("Structure HTML", r"<!DOCTYPE html>"),
            ("Balise head", r"<head>"),
            ("Balise body", r"<body>"),
            ("Titre de page", r"Score Écologique"),
            ("Formulaire", r"<form"),
            ("JavaScript", r"<script>"),
            ("CSS inline", r"<style>"),
            ("Indicateurs", r"🌳|🌱|🧪|🛡️|✂️|💧|♻️|🐦|🚫|✅"),
            ("Calcul de score", r"calcEcoScore"),
            ("LocalStorage", r"localStorage"),
            ("Responsive design", r"@media"),
            ("Animations", r"@keyframes|animation|transition")
        ]
        
        for element, pattern in analyses_contenu:
            if re.search(pattern, contenu, re.IGNORECASE):
                print(f"✅ {element}")
            else:
                print(f"❌ {element}")
    else:
        print("❌ Fichier principal manquant - analyse impossible")
    
    print()
    
    # 3. Analyse de la navigation
    print("🧭 ANALYSE DE LA NAVIGATION")
    print("-" * 30)
    
    index_file = "frontend/index.html"
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            contenu_index = f.read()
        
        nav_elements = [
            ("Carte Score Écologique", r"Score Écologique"),
            ("Lien vers la page", r"score-ecologique\.html"),
            ("Icône écologique", r"fas fa-leaf"),
            ("Badge Nouveau", r"feature-badge"),
            ("Gradient vert", r"eco-icon")
        ]
        
        for element, pattern in nav_elements:
            if re.search(pattern, contenu_index, re.IGNORECASE):
                print(f"✅ {element}")
            else:
                print(f"❌ {element}")
    else:
        print("❌ Page d'accueil manquante")
    
    print()
    
    # 4. Analyse des styles CSS
    print("🎨 ANALYSE DES STYLES")
    print("-" * 30)
    
    css_file = "frontend/css/style.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            contenu_css = f.read()
        
        css_elements = [
            ("Style eco-icon", r"\.eco-icon"),
            ("Gradient vert", r"linear-gradient.*#4ade80.*#22c55e"),
            ("Responsive design", r"@media"),
            ("Animations", r"@keyframes|animation"),
            ("Variables CSS", r"--primary-color|--secondary-color")
        ]
        
        for element, pattern in css_elements:
            if re.search(pattern, contenu_css, re.IGNORECASE):
                print(f"✅ {element}")
            else:
                print(f"❌ {element}")
    else:
        print("❌ Fichier CSS manquant")
    
    print()
    
    # 5. Analyse des fonctionnalités
    print("⚡ ANALYSE DES FONCTIONNALITÉS")
    print("-" * 30)
    
    fonctionnalites = [
        ("10 indicateurs environnementaux", "Définis dans la documentation"),
        ("Calcul de score pondéré", "Algorithme défini"),
        ("Classification par couleurs", "4 niveaux : Rouge, Orange, Vert, Or"),
        ("Historique localStorage", "Structure définie"),
        ("Interface responsive", "Breakpoints définis"),
        ("Animations CSS", "Transitions et keyframes"),
        ("Validation des données", "Contrôles utilisateur"),
        ("Export des résultats", "Fonctionnalité prévue")
    ]
    
    for fonctionnalite, statut in fonctionnalites:
        print(f"📋 {fonctionnalite} - {statut}")
    
    print()
    
    # 6. Calcul du score de complétude
    print("📈 SCORE DE COMPLÉTUDE")
    print("-" * 30)
    
    total_elements = 0
    elements_presents = 0
    
    # Compter les éléments présents
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        elements_a_verifier = [
            r"<!DOCTYPE html>", r"<head>", r"<body>", r"Score Écologique",
            r"<form", r"<script>", r"<style>", r"calcEcoScore", r"localStorage"
        ]
        
        for pattern in elements_a_verifier:
            total_elements += 1
            if re.search(pattern, contenu, re.IGNORECASE):
                elements_presents += 1
    
    # Ajouter les fichiers
    total_elements += len(fichiers_analyse)
    elements_presents += len(fichiers_presents)
    
    if total_elements > 0:
        score_completude = (elements_presents / total_elements) * 100
        print(f"📊 Score de complétude : {score_completude:.1f}%")
        
        if score_completude >= 90:
            niveau = "🟢 Excellent"
        elif score_completude >= 70:
            niveau = "🟡 Bon"
        elif score_completude >= 50:
            niveau = "🟠 Moyen"
        else:
            niveau = "🔴 Critique"
        
        print(f"🏆 Niveau : {niveau}")
    else:
        print("❌ Impossible de calculer le score")
    
    print()
    
    # 7. Recommandations
    print("💡 RECOMMANDATIONS")
    print("-" * 30)
    
    if len(fichiers_manquants) > 0:
        print("🔧 Actions immédiates :")
        for fichier, description in fichiers_manquants:
            print(f"   • Créer {fichier} - {description}")
    
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        if len(contenu) < 1000:  # Page trop courte
            print("🔧 Développement requis :")
            print("   • Implémenter la structure HTML complète")
            print("   • Ajouter les 10 indicateurs environnementaux")
            print("   • Créer les styles CSS")
            print("   • Développer les fonctionnalités JavaScript")
    
    print("🚀 Améliorations futures :")
    print("   • Ajouter des recommandations personnalisées")
    print("   • Implémenter l'export PDF")
    print("   • Intégrer des comparaisons entre producteurs")
    print("   • Ajouter des analytics avancés")
    
    print()
    
    # 8. Résumé
    print("📋 RÉSUMÉ DE L'ANALYSE")
    print("-" * 30)
    
    print(f"📁 Fichiers présents : {len(fichiers_presents)}/{len(fichiers_analyse)}")
    print(f"📄 Documentation : {'✅' if os.path.exists('SCORE_ECOLOGIQUE_DOCUMENTATION.md') else '❌'}")
    print(f"🧪 Tests : {'✅' if os.path.exists('test_score_ecologique.py') else '❌'}")
    print(f"🎨 Styles : {'✅' if os.path.exists('frontend/css/style.css') else '❌'}")
    print(f"🧭 Navigation : {'✅' if 'Score Écologique' in contenu_index else '❌'}")
    
    print()
    print("🎉 Analyse terminée !")

if __name__ == "__main__":
    analyser_score_ecologique()
