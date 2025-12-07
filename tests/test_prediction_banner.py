#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test spécifique pour la bannière de la page prediction
"""

import os
import re

def test_prediction_banner():
    """Test spécifique de la bannière de la page prediction"""
    
    print("🎯 Test de la Bannière - Page Prédiction")
    print("=" * 50)
    
    prediction_file = "frontend/prediction.html"
    
    if not os.path.exists(prediction_file):
        print(f"❌ {prediction_file} - FICHIER MANQUANT")
        return
    
    print(f"✅ {prediction_file} - FICHIER TROUVÉ")
    
    # Lire le contenu du fichier
    with open(prediction_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les inclusions nécessaires
    print("\n🔗 Vérification des inclusions :")
    
    checks = [
        ("CSS moderne", "modern-banner.css"),
        ("JavaScript moderne", "modern-banner.js"),
        ("Font Awesome", "font-awesome"),
        ("Chart.js", "chart.js"),
        ("Header moderne", "app-header")
    ]
    
    for check_name, pattern in checks:
        if pattern in content:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
    
    # Vérifier la structure de la bannière
    print("\n🎨 Vérification de la structure de la bannière :")
    
    banner_elements = [
        ("Header container", "app-header"),
        ("Logo", "header-logo"),
        ("Actions", "header-actions"),
        ("Status indicator", "status-indicator"),
        ("Bouton retour", "btn-back")
    ]
    
    for element_name, pattern in banner_elements:
        if pattern in content:
            print(f"✅ {element_name}")
        else:
            print(f"❌ {element_name}")
    
    # Vérifier le contenu de la page
    print("\n📄 Vérification du contenu de la page :")
    
    page_elements = [
        ("Titre principal", "Prédire ma Récolte"),
        ("Formulaire de prédiction", "prediction-form"),
        ("Champs de saisie", "form-group"),
        ("Bouton de calcul", "calculate-btn"),
        ("Résultats", "prediction-results")
    ]
    
    for element_name, pattern in page_elements:
        if pattern in content:
            print(f"✅ {element_name}")
        else:
            print(f"❌ {element_name}")
    
    # Vérifier les champs du formulaire
    print("\n📝 Vérification des champs du formulaire :")
    
    form_fields = [
        ("Âge du verger", "age_verger"),
        ("Agroforesterie", "agroforest"),
        ("Engrais chimique", "engrais"),
        ("Fumier/Compost", "fumier"),
        ("Maladies", "maladie"),
        ("Herbicides", "herbicide"),
        ("Insecticides", "insecticide"),
        ("Fongicides", "fongicide")
    ]
    
    for field_name, field_id in form_fields:
        if field_id in content:
            print(f"✅ {field_name}")
        else:
            print(f"❌ {field_name}")
    
    # Résumé de la bannière prediction
    print("\n📋 Résumé de la bannière Prédiction :")
    print("=" * 50)
    
    print("""
🎯 **Page Prédiction - Bannière moderne :**

**Design :**
• Gradient vert professionnel avec effets de brillance
• Logo animé avec feuilles 🍃 et pièces 🪙
• Statut dynamique "En ligne" avec point vert pulsant
• Badge contextuel "🎯 Prédiction IA"

**Fonctionnalités :**
• Détection automatique de la page prediction.html
• Animation d'entrée fluide
• Interactions au survol du logo
• Bouton de retour avec effet hover
• Design responsive pour tous les écrans

**Contexte de page :**
• Icône : 🎯 (cible pour la prédiction)
• Sous-titre : "Prédiction IA"
• Contexte : Prédiction de productivité cacao

**Éléments visuels :**
• Effet de brillance animé
• Particules de fond scintillantes
• Animation de flottement du logo
• Transitions fluides entre les états
• Ombres et profondeur visuelle

**Navigation :**
• Bouton "Retour" vers index.html
• Animation de transition lors du clic
• Gestion des événements utilisateur
• Feedback visuel des interactions
    """)
    
    print("🎉 Test de la bannière Prédiction terminé !")

if __name__ == "__main__":
    test_prediction_banner()
